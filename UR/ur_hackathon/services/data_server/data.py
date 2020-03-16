import file_installation as installation
import logging
import Coordenates
import traceback

name_file = "default.installation"

class Data:

    def __init__(self):
        self.data = []
        self.commands = {
            "timestamp": 0,
            "target_q": 1,
            "target_qd": 2,
            "target_qdd": 3,
            "target_current": 4,
            "target_moment": 5,
            "actual_q": 6,
            "actual_qd": 7,
            "actual_current": 8,
            "joint_control_output": 9,
            "actual_TCP_pose": 10,
            "actual_TCP_speed": 11,
            "actual_TCP_force": 12,
            "target_TCP_pose": 13,
            "target_TCP_speed": 14,
            "actual_digital_input_bits": 15,
            "joint_temperatures": 16,
            "actual_execution_time": 17,
            "robot_mode": 18,
            "joint_mode": 19,
            "safety_mode": 20,
            "actual_tool_accelerometer": 21,
            "speed_scaling": 22,
            "target_speed_fraction": 23,
            "actual_momentum": 24,
            "actual_main_voltage": 25,
            "actual_robot_voltage": 26,
            "actual_robot_current": 27,
            "actual_joint_voltage": 28,
            "actual_digital_output_bits": 29,
            "runtime_state": 30,
            "safety_status_bits": 31,
            "robot_status_bits": 32,
            "get_all_joint_positions": 33,
            "get_walls": 34,
            "get_info": 35,
            "get_all_joint_target_positions": 36
        }

    def get_data(self, comm_id):
        if comm_id in self.commands:
            try:
                if comm_id == "get_walls":
                    return installation.search_safety_planes(name_file)
                elif comm_id == "get_info":
                    return "[%s,%s,%s,%s]" % (self.data[8], self.data[16], self.data[28], self.data[2])
                elif comm_id == "get_all_joint_positions":
                    actual_q = str(Coordenates.get_Coordenates(self.data[self.commands["actual_q"]]))
                    target_q = str(Coordenates.get_Coordenates(self.data[self.commands["target_q"]]))
                    return "[%s, %s]" % (actual_q, target_q)
                else:
                    return self.data[self.commands[comm_id]]
            except Exception as err:
                logging.error(str(err))
                logging.error(traceback.format_exc())
        return -1
