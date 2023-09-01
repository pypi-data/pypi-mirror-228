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
    """Class to represent natural gas."""

    def __init__(self, java_natural_gas=None):
        # Local dictionary to store component and its mole percent
        if java_natural_gas is None:
            self.compo_mol_percent = {}
        else:
            if isinstance(java_natural_gas, list):
                self.compo_mol_percent = {
                    component: [
                        ng.getCompositionMolePercent(component.value) 
                        for ng in java_natural_gas
                    ] for component in Component
                }
            else:
                self.compo_mol_percent = {
                    component: java_natural_gas.getCompositionMolePercent(component.value) 
                    for component in Component
                }
        # Placeholder for java object
        self.java_natural_gas = java_natural_gas
        # Initialize java builder
        self.java_builder = None

    def add_component(self, component, mol_percent):
        """Add component to natural gas considering mole percent."""
        # Initialise java builder
        if self.java_builder is None:
            if isinstance(mol_percent, list):
                self.java_builder = [jvm.NaturalGas.Builder() for _ in mol_percent]
                # Store component locally
                self.compo_mol_percent[component] = mol_percent
            else:
                self.java_builder = jvm.NaturalGas.Builder()
                # Store component locally
                self.compo_mol_percent[component] = mol_percent
        # Add component to java builder
        if isinstance(mol_percent, list):
            for idx, mp in enumerate(mol_percent):
                self.java_builder[idx].addComponent(component.value, mp)
        else:
            self.java_builder.addComponent(component.value, mol_percent)

    def build(self):
        """Build natural gas java object."""
        if isinstance(self.java_builder, list):
            self.java_natural_gas = [builder.build() for builder in self.java_builder]
        else:
            self.java_natural_gas = self.java_builder.build()

    def get_mol_percent(self, component):
        """Get mole percent of natural gas considering component."""
        if isinstance(self.java_natural_gas, list):
            return [ng.getCompositionMolePercent(component.value) for ng in self.java_natural_gas]
        else:
            return self.java_natural_gas.getCompositionMolePercent(component.value)

    def get_amount(self, component=None, total_flow=None, to_units=None, value_only=False):
        """Get amount of natural gas considering total flow and units."""
        if isinstance(self.java_natural_gas, list):
            results = []
            for idx, ng in enumerate(self.java_natural_gas):
                quantity = jvm.Quantities.getQuantity(total_flow[0][idx], NaturalGas.__parse_units(total_flow[1]))
                if component is not None:
                    amount = ng.getAmount(component.value, quantity, NaturalGas.__parse_units(to_units))
                else:
                    amount = ng.getAmount(quantity, NaturalGas.__parse_units(to_units))
                results.append(float(amount.getValue()) if value_only else amount)
            return results
        else:
            quantity = jvm.Quantities.getQuantity(total_flow[0], NaturalGas.__parse_units(total_flow[1]))
            if component is not None:
                amount = self.java_natural_gas.getAmount(component.value, quantity, NaturalGas.__parse_units(to_units))
            else:
                amount = self.java_natural_gas.getAmount(quantity, NaturalGas.__parse_units(to_units))
            return float(amount.getValue()) if value_only else amount
            
    @staticmethod
    def blend(natural_gas_1, flow_ng_1, natural_gas_2, flow_ng_2):
        """Blend two natural gas."""
        if isinstance(natural_gas_1.java_natural_gas, list):
            return NaturalGas([
                jvm.NaturalGas.blend(
                    ng1, 
                    jvm.Quantities.getQuantity(flow_ng_1[0][idx], NaturalGas.__parse_units(flow_ng_1[1])),
                    ng2,
                    jvm.Quantities.getQuantity(flow_ng_2[0][idx], NaturalGas.__parse_units(flow_ng_2[1])),
                ) for idx, (ng1, ng2) in enumerate(zip(natural_gas_1.java_natural_gas, natural_gas_2.java_natural_gas))]
            )
        else:
            return NaturalGas(
                jvm.NaturalGas.blend(
                    natural_gas_1.java_natural_gas,
                    jvm.Quantities.getQuantity(flow_ng_1[0], NaturalGas.__parse_units(flow_ng_1[1])),
                    natural_gas_2.java_natural_gas,
                    jvm.Quantities.getQuantity(flow_ng_2[0], NaturalGas.__parse_units(flow_ng_2[1]))
                )
            )
    
    @staticmethod
    def __parse_units(units):
        """Parse units to java object."""
        # Return java object considering most common units
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
        
    def __str__(self):
        """Return string representation of natural gas."""
        if isinstance(self.java_natural_gas, list):
            return str([ng.toString() for ng in self.java_natural_gas])
        else:
            return self.java_natural_gas.toString()
        


class Component(Enum):
    """Enum class to represent natural gas components."""

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