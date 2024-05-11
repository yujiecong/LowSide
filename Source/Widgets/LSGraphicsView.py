import itertools
from typing import *

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from Source import Globs
from Source.Common import Func
from Source.Common.DataClass import LSPinConnectInfo
from Source.Common.Obj import LSDictWrapper
from Source.Common.Enums import ItemZValue, LSMimeSource
from Source.Common.Err import LSTypeError
from Source.Common.Func import OS
from Source.Common.Logger import ls_print
from Source.Custom import LSCommand
from Source.Custom.Enums.LSItemEnum import LSNodeItemType, LSPropertyType
from Source.Custom.LSGlobalData import LSIdentifierData
from Source.Custom.LSMimeData import LSMimeData
from Source.Custom.LSObject import LSObject
from Source.Custom.LSGraphicsViewParser import LSGraphicsViewParser
from Source.Custom.LSUndoStack import LSUndoStack
from Source.Widgets.NodeItem.LSAstNodeItem import LSAstNodeItem
# 这一条还真的重要 能够让 meta 识别到所有的widget

from Source.Widgets.NodeItem.LSBidirectionalItem import LSBidirectionalItem
from Source.Widgets.NodeItem.LSConnectableItem import LSConnectableItem
from Source.Widgets.NodeItem.Event.LSEventNodeItem import LSEventNodeItem
from Source.Widgets.NodeItem.Event.LSEventNodeItem_ProgramStart import LSEventNodeItem_ProgramStart
from Source.Widgets.Pin.LSFlowPin import LSFlowPin
from Source.Widgets.LSGraphicsBackgroundPixmapItem import LSGraphicsBackgroundPixmapItem
from Source.Widgets.LSGraphicsProxyWidget import LSGraphicsProxyWidget
from Source.Widgets.LSGraphicsScene import LSGraphicsScene
from Source.Widgets.LSGraphicsViewBackgroundPixmap import LSGraphicsViewBackgroundPixmap
from Source.Widgets.NodeItem.LSItem import LSItem
from Source.Widgets.NodeItem.LSNodeItem import LSNodeItem
from Source.Widgets.Common.LSPathItem import LSPathItem
from Source.Widgets.LSQuickSearchWidget import LSQuickSearchWidget

"""
我需要一个纯天然无污染的低代码控件
以后也有大作用

"""
qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSGraphicsView(QGraphicsView, LSObject):
    selectItem_signal=Signal(str, object)

    MaxZoomCount = 6
    MinZoomCount = -10
    CurrentScaleCount = 0
    ScaleFactor = 1.2

    _ViewportWidth=-99999
    _ViewportHeight=-99999
    @classmethod
    def deserialize(cls, data):
        new_view = cls()
        view_data: "LSGraphicsView" = LSDictWrapper(data)
        items = []
        items_data = view_data.items_data

        for item_data in items_data:
            wrapper_data:LSNodeItem = LSDictWrapper(item_data)
            class_type: LSNodeItem = LSObject.registered_classes[wrapper_data.type_name]
            item = class_type.deserialize(wrapper_data)
            new_view.add_item(item)
            items.append(item)

        for idx, item_data in enumerate(items_data):
            item_wrapper: LSNodeItem = LSDictWrapper(item_data)
            item: LSNodeItem = items[idx]
            for connect_info in item_wrapper.pin_connect_info:
                connect_info_wrapper: LSPinConnectInfo = LSDictWrapper(connect_info)
                "connect的那个对象不见了 可能意外被删除 那就跳过了"
                item.connect_pin_by_uuid(connect_info_wrapper.to_node_uuid,
                                         connect_info_wrapper.pin_uuid,
                                         connect_info_wrapper.to_pin_uuid)
        new_view.setSceneRect(*view_data.view_scene_rect_data)
        return new_view

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        LSObject.__init__(self)
        self.init_serialize_data()

    def init_attrs(self):
        super().init_attrs()
        # self.default_width = 600
        # self.default_height = 400

        self.current_path = None
        self.parser = LSGraphicsViewParser()
        self.undo_stack: LSUndoStack = LSUndoStack()
        self.ignore_item_types = tuple([LSGraphicsBackgroundPixmapItem])
        self.rubber_area_selected_items: List[LSNodeItem] = []
        self.ls_items: List[Optional[LSNodeItem]] = []
        self.bg_items: List[List[LSGraphicsBackgroundPixmapItem]] = []
        self.bg_pixmap_items: List[List[LSGraphicsViewBackgroundPixmap]] = []
        self.all_bg_items: List[LSGraphicsBackgroundPixmapItem] = []

        self._is_left_mouse_button_click_nothing = True
        self._right_mouse_button_pressed_pos = QPoint()
        self._right_mouse_button_moved_pos = QPoint()

        self._left_mouse_button_pressed_pos = QPoint()
        self._is_left_mouse_button_pressed = False

        self._is_right_mouse_button_pressed_moved = False
        self._is_right_mouse_button_pressed = False

        self._is_drag_ctrl_pressed=False
        self._is_drag_alt_pressed=False

        self.current_horizontal_update_count = 0
        self.current_vertical_update_count = 0

        self.total_scene_diff_pos = QPointF()
        self.current_scene_diff_pos = QPointF()

        # self.start_view_pos = QPoint(-self.default_width / 2, -self.default_height / 2)

        self.duplicated_origin_items: List[LSNodeItem] = []

        self.uuid_2_ls_item: Dict[str, LSItem] = {}

        self.is_moving_items = False
        self.is_moving = False

        self.keys_pressed = {}
        self.key_timer = QTimer(self)
        self.key_timer.timeout.connect(self.move_scene)
        self.key_timer.setInterval(10)

    def init_background(self, bg_item_row_count, bg_item_col_count):
        self.bg_item_col_count = bg_item_col_count
        self.bg_item_row_count = bg_item_row_count
        for item in self.all_bg_items:
            self.m_scene.removeItem(item)

        bg_items = []
        for i in range(-self.bg_item_row_count, self.bg_item_row_count):
            row_items = []
            pixmap_items = []
            for j in range(-self.bg_item_col_count, self.bg_item_col_count):
                pixmap_item = LSGraphicsBackgroundPixmapItem()
                self.m_scene.addItem(pixmap_item)
                row_items.append(pixmap_item)
                pixmap_items.append(pixmap_item)
            self.bg_pixmap_items.append(pixmap_items)
            bg_items.append(row_items)

        self.bg_items = bg_items
        self.all_bg_items: List[LSGraphicsBackgroundPixmapItem] = [item for item in itertools.chain(*self.bg_items)]
        self.total_count = len(self.all_bg_items)
        self.update_bg_items_pos()

    def init_properties(self):
        super().init_properties()
        # self.resize(self.default_width, self.default_height)
        "如果不设置最小尺寸的话 移动会有问题"
        # self.setMinimumSize(self.default_width,self.default_height)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.HighQualityAntialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setRenderHint(QPainter.TextAntialiasing, True)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setAcceptDrops(True)

        # self.setSceneRect(QRectF(-10000, -10000, 20000, 20000))
        # self.verticalScrollBar().setRange(-10000, 10000)
        # self.horizontalScrollBar().setRange(-10000, 10000)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        "无法交互了"
        # self.setInteractive(False)
        self.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)
        "opengl 减速"
        # self.format.setSamples(16)
        # self.gl.setFormat(self.format)
        # self.setViewport(self.gl)
        # self.setOptimizationFlag(QGraphicsView.IndirectPainting)
        # self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))
        # self.update_timer=QTimer()
        # self.update_timer.timeout.connect(lambda :self._scene.update())
        # self.update_timer.setInterval(16)
        # self.update_timer.start()

    def init_scene(self):
        self.m_scene = LSGraphicsScene()
        self.setScene(self.m_scene)

        proxy = self.m_scene.addWidget(self.quick_search_widget)
        proxy.setZValue(ItemZValue.QuickSearchWidget)
        proxy.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
        self.quick_search_widget.hide()

    def init_connection(self):
        self.quick_search_widget.tree_widget.placed_signal.connect(self.place_item)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(qss)

    def init_ui(self):
        super().init_ui()
        self.quick_search_widget = LSQuickSearchWidget()
        self.gl = QOpenGLWidget()
        self.format = QSurfaceFormat()
        self.init_scene()



    def create_variable_menu(self):
        self.variable_menu = QMenu(self)
        title_action = QWidgetAction(self)
        title_widget=QWidget()
        title_action.setDefaultWidget(title_widget)
        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(6, 5, 0, 0)
        title_widget.setLayout(title_layout)
        title_layout.addWidget(QLabel(f"{self.mime_data.name}  ────"))
        title_action.setEnabled(False)
        title_widget.setObjectName("title_action")
        title_widget.setStyleSheet("""color:rgb(104, 104, 104);font: 75 7pt "微软雅黑";;background:transparent;""")

        get_var_action = QAction(f"Get {self.mime_data.name}",self)
        set_var_action = QAction(f"Set {self.mime_data.name}",self)
        get_var_action.triggered.connect(lambda: self.place_item_from_property(LSPropertyType.Get))
        set_var_action.triggered.connect(lambda: self.place_item_from_property(LSPropertyType.Set))
        self.variable_menu.addAction(title_action)
        self.variable_menu.addAction(get_var_action)
        self.variable_menu.addAction(set_var_action)
        if self._is_drag_ctrl_pressed:
            self.place_item_from_property(LSPropertyType.Get)
        elif self._is_drag_alt_pressed:
            self.place_item_from_property(LSPropertyType.Set)
        else:
            self.variable_menu.popup(QCursor.pos())

    def init_serialize_data(self):
        def _serialize_items():
            data = []
            for item in self.ls_items:
                item_data = item.serialize()
                data.append(item_data)
            return data

        # def _viewport_values():
        #     return  [self.horizontalScrollBar().value(), self.verticalScrollBar().value()]
        def _scene_rect():
            scene_rect = self.sceneRect()
            return scene_rect.x(), scene_rect.y(), scene_rect.width(), scene_rect.height()

        with LSObject.Record(self, LSObject.RecordType.Serialize):
            self.items_data: list = _serialize_items
            # self.viewport_values =_viewport_values
            self.view_scene_rect_data = _scene_rect


    @property
    def cursor_scene_pos(self):
        scene_pos = self.mapToScene(self.mapFromGlobal(QCursor.pos())).toPoint()
        return scene_pos

    def update_bg_items_pos(self):

        center_scene_pos = QPoint()
        for i in range(-self.bg_item_row_count, self.bg_item_row_count):
            for j in range(-self.bg_item_col_count, self.bg_item_col_count):
                pos = center_scene_pos + QPoint(j * LSGraphicsViewBackgroundPixmap.Width,
                                                i * LSGraphicsViewBackgroundPixmap.Height)
                item = self.bg_items[i][j]
                item.show()
                item.setPos(pos)  # 设置图片项的位置，紧密相邻

        col_count = len(self.bg_items[0])
        row_count = len(self.bg_items)

        self.bg_item_width = (col_count) * LSGraphicsViewBackgroundPixmap.Width
        self.bg_item_height = (row_count) * LSGraphicsViewBackgroundPixmap.Height

        self.bg_item_half_width = int(self.bg_item_width / 2)
        self.bg_item_half_height = int(self.bg_item_height / 2)

        self.bg_items_pos = [item.pos() for item in self.all_bg_items]

    def update_background(self):
        scene_size = self.mapToScene(self.width(), self.height())
        col_count = int(scene_size.x() / LSGraphicsViewBackgroundPixmap.Width) + 4
        row_count = int(scene_size.y() / LSGraphicsViewBackgroundPixmap.Height) + 4
        self.init_background(row_count, col_count)
        # self.center_background_dynamic()

    def center_background_dynamic(self):
        """
        只要背景一直移动,就能看起来是移动的
        :return:
        """
        # diff_pos=scene_pos-self.mapToScene(self._RightMouseButtonPressedPos)
        #
        # self.current_scene_diff_pos=diff_pos
        # LSGraphicsViewBackgroundBigPixmap.XOffset=self.total_scene_diff_pos.x()+diff_pos.x()
        # LSGraphicsViewBackgroundBigPixmap.YOffset=self.total_scene_diff_pos.y()+diff_pos.y()
        #
        # # self.bg_item.update_pixmap()
        # bg_item_pos=center_scene_pos+(QPoint(-self.bg_item_half_width, -self.bg_item_half_height))
        # self.bg_item.setPos(bg_item_pos)

        view_width = self.width()
        view_height = self.height()
        half_view_width = view_width / 2
        half_view_height = view_height / 2
        center_scene_pos = self.mapToScene(half_view_width, half_view_height)

        # offset=LSGraphicsViewBackgroundPixmap.Height*2
        # up_limit_pos=center_scene_pos.y()-self.bg_item_half_height-offset
        # down_limit_pos=center_scene_pos.y()+self.bg_item_half_height+offset
        # right_limit_pos=center_scene_pos.x()+self.bg_item_half_width+offset
        # left_limit_pos=center_scene_pos.x()-self.bg_item_half_width-offset
        up_limit_pos = center_scene_pos.y() - self.bg_item_half_height - LSGraphicsViewBackgroundPixmap.Height
        down_limit_pos = center_scene_pos.y() + self.bg_item_half_height - LSGraphicsViewBackgroundPixmap.Height

        right_limit_pos = center_scene_pos.x() + self.bg_item_half_width + LSGraphicsViewBackgroundPixmap.Width
        left_limit_pos = center_scene_pos.x() - self.bg_item_half_width - LSGraphicsViewBackgroundPixmap.Width
        for item in self.all_bg_items:
            item_pos = item.pos()
            if item_pos.x() > right_limit_pos:
                item_pos.setX(item_pos.x() - self.bg_item_width)
            elif item_pos.x() < left_limit_pos:
                item_pos.setX(item_pos.x() + self.bg_item_width)

            if item_pos.y() < up_limit_pos:
                item_pos.setY(item_pos.y() + self.bg_item_height)
            elif item_pos.y() > down_limit_pos:
                item_pos.setY(item_pos.y() - self.bg_item_height)

            item.setPos(item_pos)
            # bg_items_pos.append(added_pos)

        # self.bg_items_pos = bg_items_pos

    def place_item(self,mime_data):
        ls_print("place", mime_data.identifier)
        identifier=mime_data.identifier
        pos=mime_data.pos
        node_data = LSIdentifierData.get(identifier)
        is_event = False
        for event_item in self.ls_items:
            if event_item.identifier == identifier and node_data.node_type == LSNodeItemType.Event:
                "将当前视角移动到这个item的位置"
                is_event = True
                break

        if is_event:
            self.center_on_item(event_item)
        else:
            "如果是 Variable item 那么要弹出 menu让他选.."
            item_type: LSNodeItem = LSObject.registered_classes[node_data.instance_type]
            item = item_type.from_identifier(identifier)
            gpw = self.add_item(item)
            gpw.setPos(pos)

        self.quick_search_widget.hide()

    def place_item_from_property(self,property_type):
        self.mime_data.identifier=Func.ls_joinPaths(self.mime_data.identifier,property_type)
        self.place_item(self.mime_data)

    def add_item(self, item: "LSNodeItem"):
        if not isinstance(item, LSItem):
            raise LSTypeError

        for event_item in self.ls_items:
            if isinstance(item, LSEventNodeItem) and event_item.identifier == item.identifier:
                ls_print(f"当前已存在相同的事件'{item.identifier}',无法添加")
                return

        self.undo_stack.push(LSCommand.LSAddItemCommand(self, [item]))
        gpw = LSGraphicsProxyWidget()
        gpw.setWidget(item)

        item.set_view(self)
        self.m_scene.addItem(gpw)
        # proxy = self.gs.addWidget(node)

        self.ls_items.append(item)
        self.uuid_2_ls_item[item.uuid_] = item
        return gpw

    def find_item_by_identifier(self, identifier) -> List[LSNodeItem]:
        items = []
        for item in self.ls_items:
            if item.identifier == identifier:
                items.append(item)
        return items

    def remove_items(self, items: List[LSConnectableItem], is_force=False):
        self.undo_stack.push(LSCommand.LSDestroyedCommand(self, items))
        with Globs.DisableRecordCommandContext():
            for item in items:
                item.destruct()
                item.hide()
                self.ls_items.remove(item)
                self.uuid_2_ls_item.pop(item.uuid_)

                if item in self.rubber_area_selected_items:
                    self.rubber_area_selected_items.remove(item)

        if is_force:
            for item in items:
                # item.proxy
                # 这个也会崩溃
                # item.deleteLater()
                "这里为什么会崩溃呢 我是搞不懂啊"
                self.m_scene.removeItem(item.proxy)

    def selected_item_nodes(self):
        return [item for item in self.ls_items if item.is_selected()]

    def clear_selected(self):
        for item in self.ls_items:
            item.set_selected(False)

    def items(self, *args, **kwargs):
        total_items = super().items(*args, **kwargs)
        ignore_items = total_items[:]
        for item in total_items:
            if isinstance(item, self.ignore_item_types):
                ignore_items.remove(item)
        return ignore_items

    def create_bidirectional_item(self, pos=QPoint(), in_pin: LSFlowPin = None, out_pin: LSFlowPin = None):
        """
        :param pos:
        :param in_pin:
        :param out_pin:
        :return:
        """
        item = LSBidirectionalItem()

        self.add_item(item)

        if in_pin and out_pin:
            # out_pin.connect_pin(item.pin)
            out_pin.connect_pin(item.pin, )
            item.pin.connect_pin(in_pin, )

        item.proxy.setPos(pos - QPoint(item.width() // 2, item.height() // 2))

        item.pin.update_connected_line()
        return item

    def duplicate(self):

        self.duplicated_origin_items = []
        for item in self.selected_item_nodes():
            item.clearFocus()
            if not item.can_be_duplicated():
                continue
            self.duplicated_origin_items.append(item)
        ls_print(f"成功复制{len(self.duplicated_origin_items)}个item")
        self.duplicated_origin_items_pos = [item.pos() for item in self.duplicated_origin_items]

        def find_top_left_and_bottom_left(points):
            top_left = QPoint(99999999, 99999999)
            bottom_right = QPoint(-99999999, -99999999)

            for point in points:
                if point.x() <= top_left.x() and point.y() <= top_left.y():
                    top_left = point

                if point.x() >= bottom_right.x() and point.y() >= bottom_right.y():
                    bottom_right = point
            return top_left, bottom_right

        def find_rectangle_center(top_left, bottom_right):
            center_x = (top_left.x() + bottom_right.x()) / 2
            center_y = (top_left.y() + bottom_right.y()) / 2
            return QPoint(center_x, center_y)

        top_left, bottom_left = find_top_left_and_bottom_left(self.duplicated_origin_items_pos)
        self.origin_center_pos = find_rectangle_center(top_left, bottom_left)

    def paste(self):
        self.duplicated_items: List[LSNodeItem] = []
        for item in self.duplicated_origin_items:
            self.duplicated_items.append(item.duplicate())

        if not self.duplicated_items:
            return
        self.undo_stack.push(LSCommand.LSDuplicateCommand(self, self.duplicated_items))
        "怎么把连接的关系保存下来"
        with Globs.DisableRecordCommandContext():
            scene_pos = self.cursor_scene_pos

            if len(self.duplicated_items) == 1:
                proxy = self.add_item(self.duplicated_items[0])
                proxy.setPos(scene_pos)
            else:
                for idx, origin_item in enumerate(self.duplicated_origin_items):
                    dup_item = self.duplicated_items[idx]
                    for origin_output_pin_idx, origin_pin in enumerate(origin_item.pins):
                        origin_pin: LSFlowPin
                        for to_pin in origin_pin.to_:
                            "找到当前连接的node"
                            to_node = to_pin.node
                            "找到当前连接的node的那个pin的索引"
                            "如果用index是不准的,. 因为pin是有dynamic的.."
                            # origin_in_pin_idx = to_pin.row#to_node.pins.index(to_pin)
                            # "找到当前是什么node的索引"
                            origin_node_idx = self.duplicated_origin_items.index(to_node)
                            # "找到复制出来的node的pin"
                            # dup_out_pin = dup_item.pins[origin_output_pin_idx]
                            # "找到复制出来的node"
                            dup_target_node = self.duplicated_items[origin_node_idx]
                            # "找到复制出来的node的pin是被什么连接的"
                            # dup_in_pin = dup_target_node.pins[origin_in_pin_idx]

                            # dup_out_pin.connect_pin(dup_in_pin)
                            dup_item.connect_pin_by_pos(dup_target_node, origin_pin.row, to_pin.row)

                self.clear_selected()
                for idx, item in enumerate(self.duplicated_items):
                    proxy = self.add_item(item)
                    pos = scene_pos - self.origin_center_pos + self.duplicated_origin_items_pos[idx]
                    proxy.setPos(pos)
                    item.set_selected(True)

        "粘贴后 pin的line的位置不对 所以要强制更新"
        self.update_item_lines(self.duplicated_items)

    def update_item_lines(self, items=None):
        items = items or self.ls_items
        "我草你阿妈 这里直接在外部 调用会崩溃"
        # Util.process_sleep(10)
        for item in items:
            for pin in item.pins:
                pin.update_connected_line()

    def get_center_scene_pos(self):
        view_width = self.width()
        view_height = self.height()
        half_view_width = view_width / 2
        half_view_height = view_height / 2
        center_scene_pos = self.mapToScene(QPoint(half_view_width, half_view_height))
        return center_scene_pos

    def center_on_item(self, item):
        sr = self.sceneRect()
        center_scene_pos = self.get_center_scene_pos()
        item_pos = item.pos()
        "item的位置和当前中心的位置都知道,只需要计算偏移多少即可"
        self.update_background()

    def move_scene(self):
        sr = self.sceneRect()
        offset = 10
        dx = 0
        dy = 0
        if self.keys_pressed.get(Qt.Key_W) or self.keys_pressed.get(Qt.Key_Up):
            dy = -offset
        if self.keys_pressed.get(Qt.Key_S) or self.keys_pressed.get(Qt.Key_Down):
            dy = offset
        if self.keys_pressed.get(Qt.Key_A) or self.keys_pressed.get(Qt.Key_Left):
            dx = -offset
        if self.keys_pressed.get(Qt.Key_D) or self.keys_pressed.get(Qt.Key_Right):
            dx = offset
        if dx == 0 and dy == 0:
            return

        self.update_background()

    def generate_code(self,start_ast):
        """
        从 开始事件作为入口
        :return:
        """
        start_item = self.find_item_by_identifier(LSEventNodeItem_ProgramStart.get_identifier())
        if not start_item:
            ls_print("没有找到开始事件")
            return
        self.parser.parse(start_item[0],start_ast)
        return start_ast

    def update_item_ast(self):
        for item in self.ls_items:
            if isinstance(item,LSAstNodeItem):
                item.update_ast()

    def check_clicked_on_item(self, item):
        if isinstance(item, QGraphicsProxyWidget):
            widget: LSItem = item.widget()
            if widget:
                if isinstance(widget, LSItem):
                    return True
        return False

    def dragEnterEvent(self, event):
        super().dragEnterEvent(event)
        if event.mimeData().hasText():
            event.acceptProposedAction()



    def dragMoveEvent(self, event):
        event.acceptProposedAction()
        if event.keyboardModifiers() & Qt.Modifier.CTRL:
            self._is_drag_ctrl_pressed=True
        elif event.keyboardModifiers() & Qt.Modifier.ALT:
            self._is_drag_alt_pressed=True
    def dropEvent(self, event):
        super().dropEvent(event)
        self.mime_data:LSMimeData = event.mimeData()
        self.mime_data.pos= self.cursor_scene_pos
        if not self.mime_data.identifier:
            raise ValueError("identifier is None")
        if self.mime_data.source==LSMimeSource.Property:
            self.create_variable_menu()
        else:
            self.place_item(self.mime_data)

        self._is_drag_ctrl_pressed=False
        self._is_drag_alt_pressed=False

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)

        "这个是控件坐标系下的屏幕坐标,并不是scene里面的坐标,所以.."
        view_pos = event.pos()
        scene_pos = self.mapToScene(view_pos)
        if event.button() == Qt.LeftButton:
            LSGraphicsView._LeftMouseButtonPressedPos = scene_pos
            self._is_left_mouse_button_pressed = True
            items: Optional[LSGraphicsProxyWidget, None, QGraphicsItem] = self.items(view_pos)
            self._is_left_mouse_button_click_nothing = True
            if items:
                "已经忽略了背景了"
                item = items[0]
                widget: LSItem = item.widget()
                if self.check_clicked_on_item(item) and LSConnectableItem.IsPressed:
                    "ue的逻辑是如果点击的是已经选中的就不清空"
                    if widget not in self.selected_item_nodes():
                        if not QApplication.keyboardModifiers() == Qt.ControlModifier:
                            self.clear_selected()
                    widget.set_selected(True)
                    self._is_left_mouse_button_click_nothing = False
                elif isinstance(widget, self.quick_search_widget.__class__):
                    "如果点击到搜索框 也要响应一下"
                    self._is_left_mouse_button_click_nothing = False
                elif isinstance(item, LSPathItem):
                    pass
            else:
                "已经用手段忽略了背景item"
                "点到背景图片了,就是点到空白的意思"
                self._is_left_mouse_button_click_nothing = True

            if self._is_left_mouse_button_click_nothing:
                self.clear_selected()
                self.quick_search_widget.hide()
            else:
                "更新item的位置,定住此时的位置"
                self.selected_item_pos_list: List[QPointF] = []
                selected_items = self.selected_item_nodes()
                for selected_node in selected_items:
                    self.selected_item_pos_list.append(selected_node.proxy.pos())

        elif event.button() == Qt.RightButton:
            self.setDragMode(QGraphicsView.NoDrag)
            self._right_mouse_button_pressed_pos = event.pos()
            self._right_mouse_button_moved_pos = event.pos()
            self._is_right_mouse_button_pressed = True
            self._is_right_mouse_button_pressed_moved = False
        elif event.button() == Qt.MiddleButton:
            items: Optional[LSGraphicsProxyWidget, None, QGraphicsItem] = self.items(view_pos)
            if items:
                "已经忽略了背景了"
                item = items[0]
                if isinstance(item, QGraphicsProxyWidget):
                    widget = item.widget()
                    if widget:
                        if isinstance(widget, LSItem):
                            self.remove_items([widget])

        # self.bg_items_pos = [item.pos() for item in self.all_bg_items]

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)

        current_view_pos = event.pos()
        scene_pos = self.mapToScene(current_view_pos)
        if self._is_right_mouse_button_pressed:
            # scene_diff_pos = (scene_pos - self.mapToScene(self._right_mouse_button_moved_pos))
            scene_diff_pos = (scene_pos - self.mapToScene(self._right_mouse_button_moved_pos))
            sr = self.sceneRect()
            viewport = self.viewport()
            # delta=QPoint(sr.x() - scene_diff_pos.x(), sr.y() - scene_diff_pos.y())
            # delta = event.pos() - self._right_mouse_button_pressed_pos
            # diff=self.mapToScene(viewport.width(),viewport.height()) - self.mapToScene(0,0)
            # print(delta)
            sr2 = QRectF(sr.x() - scene_diff_pos.x(), sr.y() - scene_diff_pos.y(), sr.width(), sr.height())
            self.setSceneRect(sr2)
            # ls_print(sr2)
            # factor = abs(self.CurrentScaleCount * self.ScaleFactor)
            # self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - scene_diff_pos.x() * factor)
            # self.verticalScrollBar().setValue(self.verticalScrollBar().value() - scene_diff_pos.y()*factor)
            self.center_background_dynamic()

            self._right_mouse_button_moved_pos = current_view_pos

            distance=Func.distance_between_points(self._right_mouse_button_pressed_pos, current_view_pos)
            if distance>5:
                self._is_right_mouse_button_pressed_moved = True
            else:
                self._is_right_mouse_button_pressed_moved = False

        elif self._is_left_mouse_button_pressed:
            "如果点击到了item 就不要进行这个操作"
            if self._is_left_mouse_button_click_nothing:
                rect = self.rubberBandRect().normalized()
                [_item.set_selected(False) for _item in self.rubber_area_selected_items]

                rubber_area_items = self.items(rect)
                for item in rubber_area_items:
                    if isinstance(item, QGraphicsProxyWidget):
                        widget: LSItem = item.widget()
                        if widget:
                            if isinstance(widget, LSItem):
                                widget.set_selected(True)
                                if widget not in self.rubber_area_selected_items:
                                    self.rubber_area_selected_items.append(widget)
                            else:
                                pass
            else:
                "如果点击到了pin 那么就不能移动了"
                if LSConnectableItem.IsPressedPin:
                    pass
                else:
                    self.moved_items = self.selected_item_nodes()
                    "如果动了 那就要保留一下原来的位置才行"
                    if self.is_moving_items is False and self.moved_items:
                        self.undo_stack.push(
                            LSCommand.LSMoveCommand(
                                self.moved_items,
                                [moved_item.pos() for moved_item in self.moved_items]
                            )
                        )
                    for idx, selected_node in enumerate(self.moved_items):
                        current_view_pos = scene_pos
                        offset_pos = self.selected_item_pos_list[idx] + (
                                current_view_pos - LSGraphicsView._LeftMouseButtonPressedPos)
                        selected_node.proxy.setPos(offset_pos)

                    self.is_moving_items = True

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.RightButton:
            self.total_scene_diff_pos += self.current_scene_diff_pos

            self._is_right_mouse_button_pressed = False
            "如果么有移动才显示这个搜索框"
            if self._is_right_mouse_button_pressed_moved:
                "如果拉动超过一个背景item的距离 那么需要更新一次背景"
            else:
                items=self.items(event.pos())
                if items and self.check_clicked_on_item(items[0]):
                    pass
                else:
                    screen_pos: QPoint = event.pos()
                    self.quick_search_widget.move(self.mapToScene(screen_pos).toPoint())
                    self.quick_search_widget.show()

        elif event.button() == Qt.LeftButton:
            # selected_item_nodes = self.selected_item_nodes()
            # if selected_item_nodes and len(selected_item_nodes)==1:
            #     self.select_item.emit(LSDetailSource.Item, LSNodeDetailData())
            self._is_left_mouse_button_pressed = False
            "重置之前选中的橡皮筋区域"
            self.rubber_area_selected_items = []
            self.is_moving_items = False
            if LSConnectableItem.IsPressedPin:
                item_at = self.itemAt(event.pos())
                if item_at is None or isinstance(item_at,self.ignore_item_types):
                    self.quick_search_widget.move(self.cursor_scene_pos)
                    self.quick_search_widget.show()
            LSConnectableItem.IsPressedPin=False


        self.setDragMode(QGraphicsView.RubberBandDrag)

    def wheelEvent(self, event: QWheelEvent):
        super().wheelEvent(event)
        "这个是让搜索框不要放大"
        if event.isAccepted():
            return
        # 捕获鼠标滚轮事件，实现动态调整缩放级别
        if event.angleDelta().y() < 0:
            if LSGraphicsView.CurrentScaleCount < LSGraphicsView.MinZoomCount:
                return
            factor = 1.0 / LSGraphicsView.ScaleFactor  # 向下滚动，缩小
            LSGraphicsView.CurrentScaleCount -= 1
            # LSGraphicsViewBackgroundPixmap.Width *= LSGraphicsView.ScaleFactor*2
            # LSGraphicsViewBackgroundPixmap.Height *= LSGraphicsView.ScaleFactor*2
        else:
            if LSGraphicsView.CurrentScaleCount > LSGraphicsView.MaxZoomCount:
                return
            factor = LSGraphicsView.ScaleFactor
            LSGraphicsView.CurrentScaleCount += 1
            "这里是放大"
        size_map = {
            1: 1,
            0: 1,
            -1: 1,
            -2: 1.1,
            -3: 1.2,
            -4: 3,
            -5: 3.5,
            -6: 4.5,
            -7: 5.5,
            -8: 5,
            -9: 6,
            -10: 6,
            -11: 6.5,
        }
        # pen_width_map={
        #      -4:2,
        #      -5:3,
        #      -6:3,
        #      -7:5,
        #      -8:6,
        #      -9:6,
        #      -10:7,
        #      -11:8,
        # }
        # scale_mapped=1
        scale_mapped = size_map.get(LSGraphicsView.CurrentScaleCount, 1)
        # pen_mapped = abs(LSGraphicsView.CurrentScaleCount)#
        # pen_mapped=pen_width_map.get(LSGraphicsView.CurrentScaleCount,1)
        # LSGraphicsViewBackgroundPixmap.PenWidth= pen_mapped
        # scale_mapped=1
        # for _ in range(abs(LSGraphicsView.CurrentScaleCount)):
        #     scale_mapped=1/factor
        # ls_print(scale_mapped)
        LSGraphicsViewBackgroundPixmap.Width = int(LSGraphicsViewBackgroundPixmap.DefaultWidth * scale_mapped)
        LSGraphicsViewBackgroundPixmap.Height = int(LSGraphicsViewBackgroundPixmap.DefaultHeight * scale_mapped)
        self.scale(factor, factor)
        self.update_background()
        rect=self.sceneRect()
        viewport = self.viewport()
        diff=self.mapToScene(viewport.width(),viewport.height()) - self.mapToScene(0,0)
        self.setSceneRect(QRectF(rect.x(), rect.y(),diff.x(),diff.y()))

        # self.init_background()
        # mapped_point = (self.mapToScene(
        #     QPoint(LSGraphicsViewBackgroundPixmap.DefaultWidth, LSGraphicsViewBackgroundPixmap.DefaultHeight))-
        #                 self.mapToScene(
        #     QPoint(0, 0)))
        # LSGraphicsViewBackgroundPixmap.Width= mapped_point.x()
        # LSGraphicsViewBackgroundPixmap.Height=mapped_point.y()
        # ls_print(mapped_point)

        ls_print(LSGraphicsView.CurrentScaleCount)

        # for item in self.all_bg_items:
        #     item.update_pixmap()
        #     item.setScale(scale_mapped)
        # item.setTransform(item.transform().scale(scale_mapped,scale_mapped))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)
        if event.isAccepted():
            return
        if event.key() == Qt.Key_C and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.duplicate()
        elif event.key() == Qt.Key_V and QApplication.keyboardModifiers() == Qt.ControlModifier:
            "粘贴时 不要触发 command 的 push 操作 不然撤回会很麻烦"
            self.paste()
        if event.key() == Qt.Key_F1:
            ls_print("debug")
        elif event.key() == Qt.Key_Delete:
            self.remove_items(self.selected_item_nodes())
        elif event.key()==Qt.Key_Space:
            self.quick_search_widget.move(self.cursor_scene_pos)
            self.quick_search_widget.show()
        elif event.key()==Qt.Key_F2:
            self.update_item_ast()
        # elif event.key() == Qt.Key_S and QApplication.keyboardModifiers() == Qt.ControlModifier:
        #     self.save(r"C:\repo\_USDQ\LowSide\Test\serialize\1.pyls")
        # elif event.key() in {Qt.Key_W, Qt.Key_S, Qt.Key_A, Qt.Key_D, Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right}:
        #     self.keys_pressed[event.key()] = True
        #     if self.key_timer.isActive() is False:
        #         self.key_timer.start()

    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)
        self.keys_pressed[event.key()] = False
        if any(self.keys_pressed.values()) is False:
            self.key_timer.stop()



    def showEvent(self, event):
        super().showEvent(event)
        "这里是真的抽象"
        QTimer.singleShot(500, self.update_item_lines)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        rect = self.sceneRect()
        viewport = self.viewport()
        self.setSceneRect(QRectF(rect.x(), rect.y(), viewport.width(), viewport.height()))
        self.update_background()


if __name__ == '__main__':
    app = QApplication()
    window = LSGraphicsView()
    window.show()
    app.exec_()
