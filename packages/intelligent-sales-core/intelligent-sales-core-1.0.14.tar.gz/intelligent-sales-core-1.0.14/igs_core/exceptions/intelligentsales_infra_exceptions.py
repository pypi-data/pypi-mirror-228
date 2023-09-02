from igs_core.singleton_metaclass.singleton import SingletonMetaClass


class IntelligentSalesException(Exception, metaclass=SingletonMetaClass):
    def __init__(self):
        self.code = None
        self.message = None


class FileKeyError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class FileKeyWarning(IntelligentSalesException):
    def __init__(self, message):
        self.code = "WARN.0.00.00"
        self.message = message


class ProviderPrefixError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class EventInfoExtractionError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANotExpectedPriceValueError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANotExpectedIDValueError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class ParamNotExistentError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class ColumnsNotFoundError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class ColumnTypeError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class ProviderSFTPNameError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DifferingMetadataBetweenFilesWarning(IntelligentSalesException):
    def __init__(self, message):
        self.code = "WAR.0.00.00"
        self.message = message


class S3ObjectNotFoundWarning(IntelligentSalesException):
    def __init__(self, message):
        self.code = "WAR.0.00.00"
        self.message = message


class WarningsFoundDuringMetadataCheckWarning(IntelligentSalesException):
    def __init__(self, message):
        self.code = "WAR.0.00.00"
        self.message = message


class FileTypeError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class NotExpectedFileTypeError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class FileDialectEncodingNotExpectedError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class UnexpectedPathToProcessedFromPrefixError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class ParsedFileError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQAYearNotExpectedError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANonIntegerValueError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANonPositiveIntegerValueError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANoPartsPerUnitError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANonDateFormatValuesError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANonDatetimeFormatError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANonInePeriodoSpecificFormatError(IntelligentSalesException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class NonStandardCSVFormattWarning(IntelligentSalesException):
    def __init__(self, message):
        self.code = "WARN.0.00.00"
        self.message = message


class SLIParsingWarning(IntelligentSalesException):
    def __init__(self, message):
        self.code = "WARN.0.00.00"
        self.message = message


class RenamedColumnsAsExpectedWarning(IntelligentSalesException):
    def __init__(self, message):
        self.code = "WARN.0.00.00"
        self.message = message
