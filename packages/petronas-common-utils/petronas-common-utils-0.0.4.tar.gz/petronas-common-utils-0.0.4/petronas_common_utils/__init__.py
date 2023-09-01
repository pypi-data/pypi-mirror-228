from petronas_common_utils.java_connector import PetronasCommonUtilsService
from py4j.java_gateway import JavaGateway


# Launch java service
petronas_common_utils = PetronasCommonUtilsService()
# Create connection to java service
gateway = JavaGateway()
# Set gateway to allow closure at end
petronas_common_utils.set_gateway(gateway)