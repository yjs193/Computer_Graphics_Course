import csv

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from loop import loop_subdiv
from draw import *
from Catnull import *
import win32con
import win32gui

m_tranlate = [0, 0, -5]  # 用于平移，对应X Y Z 平移量。按键X:上    S:下   A:左  D:右
m_rorate = [0, 0]  # 用于旋转，分别绕X轴和Y轴旋转的角度，用鼠标左键控制
m_scale = 1.0  # 用于缩放，用鼠标中间滚轮控制
m_MouseDownPT = [0, 0]  # 记录鼠标坐标点，用于控制旋转角度
m_bMouseDown = False  # 记录鼠标左键是否按下，按下为TRUE,初始值为false
line_mode = True
iteration = 1
Cat_or_loop = 0
div_type = 0
file_name = "cube_3.obj"


# 正方体
input_points = [
    [-1.0, 1.0, 1.0],
    [-1.0, -1.0, 1.0],
    [1.0, -1.0, 1.0],
    [1.0, 1.0, 1.0],
    [1.0, -1.0, -1.0],
    [1.0, 1.0, -1.0],
    [-1.0, -1.0, -1.0],
    [-1.0, 1.0, -1.0]
]

input_faces = [
    [0, 1, 2, 3],
    [3, 2, 4, 5],
    [5, 4, 6, 7],
    [7, 0, 3, 5],
    [7, 6, 1, 0],
    [6, 1, 2, 4],
]


# 锥体
# input_points = [
#     [-1.0, 1.0, 1.0],
#     [1.0, -1.0, 1.0],
#     [1.0, 1.0, -1.0],
#     [-1.0, -1.0, -1.0],
# ]
#
# input_faces = [
#     [0, 3, 1],
#     [0, 3, 2],
#     [0, 2, 1],
#     [3, 2, 1],
# ]


def load_obj(filename):
    global div_type
    vertices = []
    faces = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('v '):
                vertex = list(map(float, line.split()[1:]))
                vertices.append(vertex)
            elif line.startswith('f '):
                face = list(map(int, [i.split('/')[0] for i in line.split()[1:]]))
                faces.append(face)
    faces = [[x-1 for x in row] for row in faces]
    # print(faces)
    div_type = determine_mesh_type(faces)
    return vertices, faces


def draw_square():
    vertices, faces = load_obj('cube_4.obj')

    # input_faces = [[x+1 for x in row] for row in input_faces]
    type = determine_mesh_type(faces)
    # print(type)
    draw_obj(vertices, faces, type)


# 调用函数绘制图像事件
def display():
    global iteration
    global file_name
    light()  # 光照函数
    glClearColor(0.33, 0.33, 0.33, 0.8)  # 背景颜色
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # 擦除背景色和深度缓存
    glPushMatrix()  # 压栈
    # glTranslatef(0, 0, -100)
    glEnable(GL_COLOR_MATERIAL)  # 改变物体颜色前置代码

    glColor3f(0.4, 0.5, 0.5)  # 设置颜色
    glTranslatef(m_tranlate[0], m_tranlate[1], m_tranlate[2])  # 平移(X,Y,Z)
    glRotatef(m_rorate[0], 1, 0, 0)  # 旋转 绕X轴
    glRotatef(m_rorate[1], 0, 1, 0)  # 旋转 绕Y轴
    glScalef(m_scale, m_scale, m_scale)  # 缩放（X,Y,Z）
    # glutSolidTeapot(1.2)  # 绘制一个茶壶
    # draw_triangle()  # 绘制两个三维三角形
    # draw_square()
    # catmull(input_points, input_faces, iteration)
    # loop(input_points, input_faces, iteration)
    points, faces = load_obj(file_name)
    subdiv(div_type, points, faces, iteration)
    glPopMatrix()
    # 出栈
    glutSwapBuffers()  # 交换前后缓冲区


def subdiv(div_type, input_points, input_faces, iterations):
    if div_type == 4:
        print(f"Catmull-Clark细分{iterations}次")
        catmull(input_points, input_faces, iterations)
    elif div_type == 3:
        print(f"Loop细分{iterations}次")
        loop(input_points, input_faces, iterations)


def catmull(input_points, input_faces, iterations):
    output_points, output_faces = input_points, input_faces
    for i in range(iterations):
        output_points, output_faces = cmc_subdiv(output_points, output_faces)
    with open('catmull_output.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for row in output_points:
            csv_writer.writerow(row)
    draw_obj(output_points, output_faces, 4)


def loop(input_points, input_faces, iterations):
    output_points, output_faces = input_points, input_faces
    for i in range(iterations):
        output_points, output_faces = loop_subdiv(output_points, output_faces)
    with open('loop_output.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for row in output_points:
            csv_writer.writerow(row)
    draw_obj(output_points, output_faces, 3)


# 窗口大小改变事件
def ReshapeEvent(width, height):  # 窗口大小改变事件
    glViewport(0, 0, width, height)  # 视口在屏幕的大小位置
    glMatrixMode(GL_PROJECTION)  # 投影矩阵
    glLoadIdentity()  # 单位矩阵
    gluPerspective(45.0, width / height, 0.1, 10000.0)  # 设置投影矩阵
    glMatrixMode(GL_MODELVIEW)  # 模型矩阵
    glLoadIdentity()  # 单位矩阵
    glEnable(GL_DEPTH_TEST)  # 启动深度检查


# 光源函数
def light():
    ambientlight0Color = (0.0, 0.0, 0.0, 1.0)
    diffuselight0Color = (1.0, 1.0, 1.0, 1.0)
    specularlight0Color = (1.0, 1.0, 1.0, 1.0)
    light0Position = (-2.0, 2.0, 2.0, 1.0)
    ambientM = (0.11, 0.06, 0.11, 1.0)
    ambientD = (0.43, 0.47, 0.54, 1.0)
    ambientS = (0.33, 0.33, 0.52, 1.0)
    ambientE = (0.0, 0.0, 0.0, 0.0)
    ambientSE = 10
    # 设置光源
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientlight0Color)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuselight0Color)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specularlight0Color)
    glLightfv(GL_LIGHT0, GL_POSITION, light0Position)
    # 设置材质
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambientM)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, ambientD)
    glMaterialfv(GL_FRONT, GL_SPECULAR, ambientS)
    glMaterialfv(GL_FRONT, GL_EMISSION, ambientE)
    glMaterialf(GL_FRONT, GL_SHININESS, 10.0)
    # 启动光照
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)


# 空闲事件
def IdleEvent():
    glutPostRedisplay()


# 键盘事件 上下左右键
def KeyboardEvent(key, x, y):
    global m_tranlate
    if (key == b'W' or key == b'w'):
        m_tranlate[1] += 0.1  # 上移动
    elif (key == b'S' or key == b's'):
        m_tranlate[1] -= 0.1  # 下移动
    elif (key == b'A' or key == b'a'):
        m_tranlate[0] -= 0.1  # 左移动
    elif (key == b'D' or key == b'd'):
        m_tranlate[0] += 0.1  # 右移动
    elif (key == b'X' or key == b'x'):
        global line_mode
        if not line_mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # 线框模式
            line_mode = not line_mode
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # 默认模式
            line_mode = not line_mode


# 鼠标事件， 缩放
def MouseEvent(button, state, x, y):
    global m_scale
    if (state == GLUT_UP):  # 内部应用加global声明其为全局变量
        if (button == 3):  # 滚轮往上滚动
            m_scale += 0.1
        elif (button == 4):  # 滚轮往下滚动
            m_scale -= 0.1
            if (m_scale < 0.1):
                m_scale = 0.1

    # 检测鼠标左键是否按下
    global m_bMouseDown
    global m_MouseDownPT
    if (state == GLUT_DOWN and button == GLUT_LEFT_BUTTON):  # 鼠标左键按下
        m_bMouseDown = True  # 鼠标左键按下
        m_MouseDownPT[0] = x  # 记录当前X坐标
        m_MouseDownPT[1] = y  # 记录当前Y坐标
    else:
        m_bMouseDown = False  # 鼠标左键弹起，结束旋转


# 按下鼠标按钮移动鼠标事件
def MotionEvent(x, y):
    global m_rorate
    global m_MouseDownPT
    if (m_bMouseDown == True):  # 如果鼠标左键被按下
        m_rorate[0] += y - m_MouseDownPT[1]  # 通过滑动鼠标改变旋转的角度
        m_rorate[1] += x - m_MouseDownPT[0]  # 通过滑动鼠标改变旋转的角度
        m_MouseDownPT[0] = x  # 记录当前X坐标
        m_MouseDownPT[1] = y  # 记录当前Y坐标


# 点击菜单响应事件
def MenuEvent(choose):
    global m_scale
    global m_bMouseDown
    if (choose == 1):  # 复位：把旋转平移缩放的值复位
        # 用于平移，对应X Y Z 平移量。按键W:上  S:下   A:左  D：右
        m_tranlate[0] = 0
        m_tranlate[1] = 0
        m_tranlate[2] = -10

        # 用于旋转，分别是绕X轴 和Y轴旋转的角度，用鼠标左键控制
        m_rorate[0] = 0
        m_rorate[1] = 0

        # 用于缩放，用鼠标中间滚轮控制
        m_scale = 1.0

        # 记录鼠标坐标点，用于控制旋转角度；
        m_MouseDownPT[0] = 0
        m_MouseDownPT[1] = 0

        # 记录鼠标左键是否按下，按下为true,初始值为false

        m_bMouseDown = False


def set_window_topmost(window_handle):
    win32gui.SetWindowPos(window_handle, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


def main():
    global iteration
    global Cat_or_loop
    global div_type
    # div_type = determine_mesh_type(input_faces)
    iteration = int(input("请输出细分次数: "))
    # user_input = simpledialog.askstring("", "细分次数:")
    # iteration = int(user_input)
    # print(iteration)

    glutInit()  # 使用glut库初始化OpenGL
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)

    glutInitWindowPosition(0, 0)  # 窗口位置
    glutInitWindowSize(800, 800)  # 窗口尺寸
    glutCreateWindow(b"Window")  # b后加窗口名字，固定格式
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    window_handle = win32gui.GetActiveWindow()

    # 将窗口置顶
    set_window_topmost(window_handle)
    # -------------注册回调函数---------------------
    glutDisplayFunc(display)  # 调用函数绘制图像
    glutKeyboardFunc(KeyboardEvent)  # 按键事件
    glutMouseFunc(MouseEvent)  # 鼠标事件
    glutMotionFunc(MotionEvent)  # 按下鼠标按键移动鼠标事件
    glutReshapeFunc(ReshapeEvent)  # 窗口大小发生变化
    glutIdleFunc(IdleEvent)  # 空闲时间
    glutCreateMenu(MenuEvent)  # 创建菜单
    glutAddMenuEntry(b"Reset", 1)  # 菜单项1 复位

    glutAttachMenu(GLUT_RIGHT_BUTTON)  # 鼠标右键按下弹出菜单
    glutMainLoop()  # 主循环


if __name__ == '__main__':
    main()
