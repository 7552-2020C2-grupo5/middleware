class Config:
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {"development": DevelopmentConfig, "production": ProductionConfig}

# Flask-Restplus settings
RESTX_SWAGGER_UI_DOC_EXPANSION = "list"
RESTX_VALIDATE = True
RESTX_MASK_SWAGGER = False
RESTX_ERROR_404_HELP = False
