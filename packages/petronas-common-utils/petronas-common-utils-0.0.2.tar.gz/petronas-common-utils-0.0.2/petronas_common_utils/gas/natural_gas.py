from enum import Enum
from py4j.java_gateway import java_import
from petronas_common_utils import gateway

# Get java view
jvm = gateway.new_jvm_view()
# Import all required classes
java_import(jvm, 'tech.units.indriya.quantity.Quantities')
java_import(jvm, 'com.petronas.gas.NaturalGas')
java_import(jvm, 'com.petronas.EssentialUnits')


class NaturalGas:

    def __init__(self):
        # Local dictionary to store component and its mole percent
        self.__compo_mol_percent = {}
        # Placeholder for java object
        self.java_natural_gas = None
        # Initialize java builder
        self.java_builder = jvm.NaturalGas.Builder()

    def add_component(self, component, mol_percent):
        # Store component locally
        self.__compo_mol_percent[component] = mol_percent
        # Add component to java builder
        self.java_builder.addComponent(component.value, mol_percent)

    def build(self):
        self.java_natural_gas = self.java_builder.build()

    def get_mol_percent(self, component):
        return self.java_natural_gas.getCompositionMolePercent(component.value)

    def get_amount(self, component=None, total_flow=None, to_units=None):
        quantity = jvm.Quantities.getQuantity(
            total_flow[0],
            self.__parse_units(total_flow[1])
        )
        return self.java_natural_gas.getAmount(
            component.value,
            quantity,
            self.__parse_units(to_units)
        )
    
    def __parse_units(self, units):
        if units in ('tph', 'TPH', 't/h', 'T/H'):
            return jvm.EssentialUnits.TONNE_PER_HOUR
        elif units in ('kgph', 'KGPH', 'kg/h', 'KG/H'):
            return jvm.EssentialUnits.KILOGRAM_PER_HOUR
        elif units in ('m3ph', 'M3PH', 'm3/h', 'M3/H'):
            return jvm.EssentialUnits.CUBIC_METRE_PER_HOUR
        elif units in ('mmscfd', 'MMSCFD'):
            return jvm.EssentialUnits.MMSCFD
        elif units in ('mmbtud', 'MMBTUD'):
            return jvm.EssentialUnits.MMBTUD
        


class Component(Enum):

    C1 = (jvm.NaturalGas.Component.C1)
    C2 = (jvm.NaturalGas.Component.C2)
    C3 = (jvm.NaturalGas.Component.C3)
    C4 = (jvm.NaturalGas.Component.C4)
    C5 = (jvm.NaturalGas.Component.C5)
    CO2 = (jvm.NaturalGas.Component.CO2)

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj