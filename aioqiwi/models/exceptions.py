class ModelConversionError(Exception):
    """
    Error occurred while json->aioqiwi.Model conversion
    """

    def __init__(self, model_type, json):
        self.json = json
        message = "Model conversion failed model=%s json=%s" % (model_type, json)
        super().__init__(message)
