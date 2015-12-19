from janitoo_manager.app import create_app
from janitoo_manager.configs.production import ProductionConfig

janitoo_manager = create_app(config=ProductionConfig())
