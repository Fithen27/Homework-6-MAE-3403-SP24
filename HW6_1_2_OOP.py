from HW6_1_OOP import ResistorNetwork, Resistor, Loop, VoltageSource
from scipy.optimize import fsolve
#endregion

#region class definitions
class ResistorNetwork2(ResistorNetwork):
    #region constructor
    def __init__(self):
        super().__init__()
        """
        The resistor network consists of Loops, Resistors and Voltage Sources.
        This is the constructor for the network and it defines fields for Loops, Resistors and Voltage Sources.
        You can populate these lists manually or read them in from a file.
        """
        #create some instance variables that are logical parts of a resistor network
        self.Loops = []  # initialize an empty list of loop objects in the network
        self.Resistors = []  # initialize an empty a list of resistor objects in the network
        self.VSources = []  # initialize an empty a list of source objects in the network
    #endregion

    def AnalyzeCircuit(self):
        """
        Use fsolve to find currents in the resistor network.
        1. KCL:  The total current flowing into any node in the network is zero.
        2. KVL:  When traversing a closed loop in the circuit, the net voltage drop must be zero.
        :return: a list of the currents in the resistor network
        """
        # need to set the currents to that Kirchoff's laws are satisfied
        i0 = [1,1,1,1,1]  # Initial guess for the currents in the circuit
        i = fsolve(self.GetKirchoffVals, i0)
        print("RN2 I1 = {:0.1f}A".format(i[0]))
        print("RN2 I2 = {:0.1f}A".format(i[1]))
        print("RN2 I3 = {:0.1f}A".format(i[2]))
        print("RN2 I4 = {:0.1f}A".format(i[3]))
        print("RN2 I5 = {:0.1f}A".format(i[4]))
        return i

    def GetKirchoffVals(self, i):
        """
        This function uses Kirchoff Voltage and Current laws to analyze this specific circuit
        KVL:  The net voltage drop for a closed loop in a circuit should be zero
        KCL:  The net current flow into a node in a circuit should be zero
        :param i: a list of currents relevant to the circuit
        :return: a list of loop voltage drops and node currents
        """

        self.GetResistorByName('ad').Current = i[0]
        self.GetResistorByName('bc').Current = i[0]
        self.GetResistorByName('ce').Current = i[1]  # Fix index here
        self.GetResistorByName('de').Current = i[2]  # Fix index here
        self.GetResistorByName('cd').Current = i[3]
        Node_c_Current = sum([i[1], i[3], -i[0]])  # Adjust indices here
        Node_d_Current = sum([-i[1], i[3], -i[0], i[2]])  # Adjust indices here

        KVL = self.GetLoopVoltageDrops()  # two equations here
        KVL.append(Node_c_Current)
        KVL.append(Node_d_Current)

        return KVL
#endregion

# region Function Definitions
def main():
    """
    This program solves for the unknown currents in the circuit of the homework assignment.
    :return: nothing
    """
    Net = ResistorNetwork2()
    Net.BuildNetworkFromFile("ResistorNetwork2.txt")
    IVals = Net.AnalyzeCircuit()
# endregion

# region function calls
if __name__=="__main__":
    main()
# endregion