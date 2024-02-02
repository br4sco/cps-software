from .controllerbase import ControllerBase, register_command

SERVO_INDEX_LOOKUP = {
    "BR_INNER_SHOULDER": 1,
    "BR_OUTER_SHOULDER": 2,
    "FR_ELBOW":          3,
    "FR_INNER_SHOULDER": 4,
    "BR_ELBOW":          5,
    "FR_OUTER_SHOULDER": 6,
    "BL_OUTER_SHOULDER": 7,
    "FL_INNER_SHOULDER": 8,
    "BL_INNER_SHOULDER": 9,
    "FL_ELBOW":          10,
    "FL_OUTER_SHOULDER": 11,
    "BL_ELBOW":          12,
}

SERVO_ORDER = [
    "FR_INNER_SHOULDER",
    "FR_OUTER_SHOULDER",
    "FR_ELBOW",
    "FL_INNER_SHOULDER",
    "FL_OUTER_SHOULDER",
    "FL_ELBOW",
    "BR_INNER_SHOULDER",
    "BR_OUTER_SHOULDER",
    "BR_ELBOW",
    "BL_INNER_SHOULDER",
    "BL_OUTER_SHOULDER",
    "BL_ELBOW",
]

ALL_SERVO_IDS = [SERVO_INDEX_LOOKUP[name] for name in SERVO_ORDER]


REGISTRY = dict()
register_read = lambda *args, **kwargs: register_command(REGISTRY, *args, kind="read", **kwargs)
register_write = lambda *args, **kwargs: register_command(REGISTRY, *args, kind="write", **kwargs)


class SpiderController(ControllerBase):
    def __init__(self, dev_dxl="/dev/ttyUSB0", dev_accel="/dev/i2c-1"):
        super().__init__(REGISTRY)
        from ..interface.dynamixel import DynamixelHandler
        from mi_cps import Accelerometer
        self.dev_dxl = dev_dxl
        self.dev_accel = dev_accel
        #self.dxl_handler = DynamixelHandler(dev_dxl)
        #self.accel_handler = Accelerometer(dev_accel)

    @register_read()
    def get_servos(self):
        return SERVO_ORDER

    @register_read()
    def read_all_servo_positions(self):
        return self.dxl_handler.read_servo_positions(ALL_SERVO_IDS)

    @register_read(argtypes=[str])
    def read_single_servo_position(self, name):
        return self.dxl_handler.read_servo_positions(SERVO_INDEX_LOOKUP[name])

    @register_read()
    def read_accel(self):
        return [
            self.accel_handler.read_accel_x(),
            self.accel_handler.read_accel_y(),
            self.accel_handler.read_accel_z()
        ]

    @register_read()
    def read_gyro(self):
        return [
            self.accel_handler.read_gyro_x(),
            self.accel_handler.read_gyro_y(),
            self.accel_handler.read_gyro_z()
        ]
