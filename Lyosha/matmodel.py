import numpy as np
import lyosha.read_data as read_data
import seaborn as sns
from matplotlib import pyplot as plt

direct = "E:\\DRIVE\\Projects\\Ending\\NTI2020\\SS\\task2\\Data\\dataframes"
cols = ['#', 'date', "oC", 'vsu', 'W', '%', 'Hours']
index = ['date']

key = 'oC'

def linear_coef(keyx, keyy, sort_key=True):
    if sort_key:
        sorted = learn_data.sort_values(keyy)
    else:
        sorted = learn_data.sort_values(keyx)
    x1 = sorted[keyx][0]
    x2 = sorted[keyx][len(sorted[keyx]) - 1]
    y1 = sorted[keyy][0]
    y2 = sorted[keyy][len(sorted[keyy]) - 1]
    dy = y1 - y2
    dx = x2 - x1
    a = dy / dx
    b = (x1 * y2 - x2 * y1) / dx
    return a, b


def dy_dx(keyx, keyy, sort_key=True):
    if sort_key:
        sorted = learn_data.sort_values(keyy)
    else:
        sorted = learn_data.sort_values(keyx)
    return (sorted[keyy][len(sorted[keyy]) - 1] - sorted[keyy][0]) / (
            sorted[keyx][len(sorted[keyx]) - 1] - sorted[keyx][0]
    )


def flinear(keyx, a, b, w=1):
    return w * a * learn_data[keyx] + b


def vlinear(x, a, b, w=1):
    return w * a * x + b


def fcos(keyx, a, A, b, B, w=1.2):
    return A * np.cos(w * a * learn_data[keyx] + b) + B


def vcos(x, a, A, b, B, w=1.2):
    return A * np.cos(w * a * learn_data[keyx] + b) + B


def fexp(keyx, a, A):
    return A * np.exp(a * learn_data[keyx])


def fquad(keyx, A, B, C):
    return A * learn_data[keyx] ** 2 + B * learn_data[keyx] + C


def max_min(out, min, max):
    for i, y in enumerate(out):
        if y < min:
            out[i] = min
        elif y > max:
            out[i] = max


model = [
    {
        "oC": ["lin", "Hours", -0.004763948497854074, 185.4558369098711],
        "%": ["cos", "oC", 60, np.radians(-40), 50],
        "W": ["lin", "%", -0.0054600000000000004, -0.254],
        "vsu": ["cos", "oC", 0.038, np.radians(90), 0.58, 25]
    },
    {
        "oC": ["lin", "Hours", -0.006207407407407404, 260.3648444444445],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
    },
    {
        "oC": ["lin", "Hours", -0.005314685314685317, 435.8760839160841],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
    },
    {
        "oC": ["lin", "Hours", -0.011303258145363421, 912.478421052633],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
    },
    {
        "oC": ["lin", "Hours", -0.007256235827664398, 135.80163265306126],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
    },
    {
        "oC": ["lin", "Hours", -0.005757575757575755, 365.90484848484886],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
    },
    {
        "oC": ["lin", "Hours", -0.0034529147982062815, -14.553766816143543],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
    },
    {
        "oC": ["lin", "Hours", -0.0060301507537688466, 389.41155778894426],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
    },
    {
        "oC": ["lin", "Hours", -0.006207407407407404, 260.3648444444445],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
    },
    {
        "oC": ["lin", "Hours", -0.006207407407407404, 260.3648444444445],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
    },
    {
        "oC": ["lin", "Hours", -0.006207407407407404, 260.3648444444445],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
    },
    {
        "oC": ["lin", "Hours", -0.006207407407407404, 260.3648444444445],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
        "oC": ["lin", "Hours", 0.006207407407407404, -260.25],
    },
]


data = read_data.Data()
data.read_from_dir(direct)
data.read(cols, index, ["#", 'Hours'])
print(123)
mask = data.data["#"] == 2
learn_data = data.data[mask]
sns.pairplot(learn_data[["oC", 'vsu', 'W', '%', 'Hours']], diag_kind="kde")
plt.show()
keyx = 'Hours'
keyy = 'oC'
a, b = linear_coef(keyx, keyy, False)
# y = fcos('oC', 'vsu', 0.038, np.radians(90), 0.58, 25)
y = flinear(keyx, a, b)
print(a, ',', b)
# y = fquad(keyx, 1e-5, 1e-1, 0)
plt.plot(learn_data[keyx], -1 * y)
plt.scatter(learn_data[keyx], learn_data[keyy])
plt.show()
