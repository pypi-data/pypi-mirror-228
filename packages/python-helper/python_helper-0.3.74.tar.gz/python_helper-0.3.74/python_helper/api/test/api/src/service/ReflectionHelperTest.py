from python_helper import ObjectHelper, StringHelper, SettingHelper, Constant, log, ReflectionHelper, Test

# LOG_HELPER_SETTINGS = {
#     log.LOG : True,
#     log.SUCCESS : True,
#     log.SETTING : True,
#     log.DEBUG : True,
#     log.WARNING : True,
#     log.WRAPPER : True,
#     log.FAILURE : True,
#     log.ERROR : True,
    # log.TEST : False
# }

LOG_HELPER_SETTINGS = {
    log.LOG : False,
    log.SUCCESS : False,
    log.SETTING : False,
    log.DEBUG : False,
    log.WARNING : True,
    log.WRAPPER : False,
    log.FAILURE : False,
    log.ERROR : False,
    log.TEST : False
}

TEST_SETTINGS = {}

@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True,
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
    },
    **TEST_SETTINGS
)
def isNotMethodInstance_withSuccess() :
    # Arrange
    class MyObject:
        def __init__(self, myAttribute) :
            self.myAttribute = myAttribute
        def myMethod(self):
            return self.myAttribute
    class MyOtherObject:
        def __init__(self, myAttribute) :
            self.myAttribute = myAttribute
            self.myHiddenAttribute = 2
        def myMethod(self):
            return self.myAttribute
    myObject = ReflectionHelper.instanciateItWithNoArgsConstructor(MyObject)
    myOtherObject = ReflectionHelper.instanciateItWithNoArgsConstructor(MyObject)
    MY_ATTRIBUTE_NAME = 'myAttribute'
    MY_METHOD_NAME = 'myMethod'
    MY_NOT_EXISTING_ATTRIBUTE_OR_METHOD_NAME = 'myNotExistingMethodOrAtrributeName'

    # Act
    attributeOrMethodNameList = ReflectionHelper.getAttributeOrMethodNameList(myObject.__class__)
    attributeNameList = ReflectionHelper.getAttributeNameList(myObject.__class__)
    methodNameList = ReflectionHelper.getMethodNameList(myObject.__class__)
    myAttribute = getattr(myObject, MY_ATTRIBUTE_NAME)
    myMethod = getattr(myObject, 'myMethod')

    # Assert
    assert [MY_ATTRIBUTE_NAME, MY_METHOD_NAME] == attributeOrMethodNameList
    assert [MY_ATTRIBUTE_NAME] == attributeNameList
    assert [MY_METHOD_NAME] == methodNameList
    assert ReflectionHelper.isNotMethodInstance(myAttribute)
    assert not ReflectionHelper.isNotMethodInstance(myMethod)
    assert ReflectionHelper.isNotMethodInstance(ReflectionHelper.getAttributeOrMethod(myObject, MY_NOT_EXISTING_ATTRIBUTE_OR_METHOD_NAME))

    assert ReflectionHelper.isNotMethod(myObject, MY_ATTRIBUTE_NAME)
    assert not ReflectionHelper.isNotMethod(myObject, MY_METHOD_NAME)
    assert ReflectionHelper.isNotMethod(myObject, MY_NOT_EXISTING_ATTRIBUTE_OR_METHOD_NAME)

    assert ReflectionHelper.isMethodInstance(myMethod)
    assert not ReflectionHelper.isMethodInstance(myAttribute)
    assert not ReflectionHelper.isMethodInstance(ReflectionHelper.getAttributeOrMethod(myObject, MY_NOT_EXISTING_ATTRIBUTE_OR_METHOD_NAME))

    assert not ReflectionHelper.isMethod(myObject, MY_ATTRIBUTE_NAME)
    assert ReflectionHelper.isMethod(myObject, MY_METHOD_NAME)
    assert not ReflectionHelper.isMethod(myObject, MY_NOT_EXISTING_ATTRIBUTE_OR_METHOD_NAME)

@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True,
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
    },
    **TEST_SETTINGS
)
def instanciateItWithNoArgsConstructor_withSuccess() :
    # Arrange
    class MyObject:
        def __init__(self, myAttribute) :
            self.myAttribute = myAttribute
    class MyOtherObject:
        def __init__(self, myAttribute, myArg, myKeyword=None) :
            self.myAttribute = myAttribute
            self.myHiddenAttribute = 2
    # from python_framework import Enum, EnumItem
    # @Enum(associateReturnsTo='number')
    # class WeekDayEnumeration :
    #     MONDAY = EnumItem(number=0)
    #     TUESDAY = EnumItem(number=1)
    #     WEDNESDAY = EnumItem(number=2)
    #     THURSDAY = EnumItem(number=3)
    #     FRIDAY = EnumItem(number=4)
    #     SATURDAY = EnumItem(number=5)
    #     SUNDAY = EnumItem(number=6)
    # WeekDay = WeekDayEnumeration()
    # class MyEnumOtherObject:
    #     def __init__(self, myAttribute=None, enum=None, myKeyword=None) :
    #         self.myAttribute = myAttribute
    #         self.myEnum = WeekDay.map(enum)
    # myEnumOtherObject = ReflectionHelper.instanciateItWithNoArgsConstructor(MyOtherObject)

    # Act
    myObject = ReflectionHelper.instanciateItWithNoArgsConstructor(MyObject)
    myOtherObject = ReflectionHelper.instanciateItWithNoArgsConstructor(MyOtherObject)

    # Assert
    assert ObjectHelper.isNotNone(myObject)
    assert ObjectHelper.isNone(myObject.myAttribute)
    assert ObjectHelper.isNotNone(myOtherObject)
    assert ObjectHelper.isNone(myOtherObject.myAttribute)
    assert 2 == myOtherObject.myHiddenAttribute

@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True,
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
    },
    **TEST_SETTINGS
)
def overrideSignatures_withSuccess() :
    # Arrange
    class MyObject:
        def myMethod(self, something):
            return something

    def myWrapper(myFunction,*wrapperAgrs,**wrapperKwargs):
        def myInBetweenWrapperFunction(*agrs,**kwargs) :
            return myFunction(*agrs,**kwargs)
        ReflectionHelper.overrideSignatures(myInBetweenWrapperFunction, myFunction)
        return myInBetweenWrapperFunction

    def myWrapperWithoutOverride(myFunction,*wrapperAgrs,**wrapperKwargs):
        def myInBetweenWrapperFunction(*agrs,**kwargs) :
            return myFunction(*agrs,**kwargs)
        return myInBetweenWrapperFunction

    OVERRIDED = '__overrided'
    NOT_OVERRIDED = '__not_overrided'

    @myWrapper
    def myOverridedFunction(arg) :
        return f'{arg}{OVERRIDED}'

    @myWrapperWithoutOverride
    def myNotOverridedFunction(arg) :
        return f'{arg}{NOT_OVERRIDED}'

    ABCD = 'abcd'
    exception = None

    # Act
    myObject = ReflectionHelper.instanciateItWithNoArgsConstructor(MyObject)
    ReflectionHelper.setAttributeOrMethod(myObject, myOverridedFunction.__name__, myOverridedFunction)
    ReflectionHelper.setAttributeOrMethod(myObject, myNotOverridedFunction.__name__, myNotOverridedFunction)
    try :
        myObject.myNotOverridedFunction('any arg')
    except Exception as e :
        exception = e

    # Assert
    assert myObject.myMethod(True)
    assert not myObject.myMethod(False)
    assert ObjectHelper.isNotNone(myOverridedFunction(True))
    assert ObjectHelper.isNotNone(myOverridedFunction(False))
    assert ObjectHelper.isNotNone(myOverridedFunction(ABCD))
    assert ObjectHelper.isNotNone(myNotOverridedFunction(True))
    assert ObjectHelper.isNotNone(myNotOverridedFunction(False))
    assert ObjectHelper.isNotNone(myNotOverridedFunction(ABCD))
    assert ObjectHelper.isNotNone(myObject.myOverridedFunction(True))
    assert ObjectHelper.isNotNone(myObject.myOverridedFunction(False))
    assert ObjectHelper.isNotNone(myObject.myOverridedFunction(ABCD))
    assert myOverridedFunction(True) == myObject.myOverridedFunction(True)
    assert myOverridedFunction(False) == myObject.myOverridedFunction(False)
    assert myOverridedFunction(ABCD) == myObject.myOverridedFunction(ABCD)
    assert f'{True}{OVERRIDED}' == myObject.myOverridedFunction(True)
    assert f'{False}{OVERRIDED}' == myObject.myOverridedFunction(False)
    assert f'{ABCD}{OVERRIDED}' == myObject.myOverridedFunction(ABCD)
    assert ObjectHelper.isNotNone(exception)
    assert "'MyObject' object has no attribute 'myNotOverridedFunction'" == str(exception)
    assert ObjectHelper.isNotNone(myObject.myInBetweenWrapperFunction(True))
    assert ObjectHelper.isNotNone(myObject.myInBetweenWrapperFunction(False))
    assert ObjectHelper.isNotNone(myObject.myInBetweenWrapperFunction(ABCD))
    assert myNotOverridedFunction(True) == myObject.myInBetweenWrapperFunction(True)
    assert myNotOverridedFunction(False) == myObject.myInBetweenWrapperFunction(False)
    assert myNotOverridedFunction(ABCD) == myObject.myInBetweenWrapperFunction(ABCD)
    assert f'{True}{NOT_OVERRIDED}' == myObject.myInBetweenWrapperFunction(True)
    assert f'{False}{NOT_OVERRIDED}' == myObject.myInBetweenWrapperFunction(False)
    assert f'{ABCD}{NOT_OVERRIDED}' == myObject.myInBetweenWrapperFunction(ABCD)

@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True,
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
    },
    **TEST_SETTINGS
)
def getArgsOrder_withSuccess() :
    # Arrange
    class MyClass :
        def __init__(
            self,
            attributeValue,
            otherAttributeValue,
            otherAttributeValueAgain,
            someOtherAttributeValue,
            otherAttributeValueOnceAgain
        ):
            self.attributeKey = attributeValue
            self.otherAttributeKey = otherAttributeValue
            self.otherAttributeKeyAgain = otherAttributeValueAgain
            self.someOtherAttributeKey = someOtherAttributeValue
            self.otherAttributeKeyOnceAgain = otherAttributeValueOnceAgain
    class MyClassWithoutAttributes :
        def __init__(self):
            ...
    class MyClassWithMoreAttributesThanArgs :
        def __init__(self,attributeValue):
            self.attributeKey = attributeValue
            self.otherAttributeKey = None
            self.otherAttributeKeyAgain = None
            self.someOtherAttributeKey = None
            self.otherAttributeKeyOnceAgain = None
    class MyClassWithLessAttributesThanArgs :
        def __init__(
            self,
            attributeValue,
            otherAttributeValue,
            otherAttributeValueAgain,
            someOtherAttributeValue,
            otherAttributeValueOnceAgain
        ):
            self.attributeKey = attributeValue
    class MyClassWithoutInitMethod :
        attributeKey = None
        otherAttributeKey = None
        otherAttributeKeyAgain = None
        someOtherAttributeKey = None
        otherAttributeKeyOnceAgain = None

    # Act
    myClassArgsOrder = ReflectionHelper.getArgsOrder(MyClass)
    myClassWithoutAttributesArgsOrder = ReflectionHelper.getArgsOrder(MyClassWithoutAttributes)
    myClassWithMoreAttributesThanArgsArgsOrder = ReflectionHelper.getArgsOrder(MyClassWithMoreAttributesThanArgs)
    myClassWithLessAttributesThanArgsArgsOrder = ReflectionHelper.getArgsOrder(MyClassWithLessAttributesThanArgs)
    myClassWithoutInitMethodArgsOrder = ReflectionHelper.getArgsOrder(MyClassWithoutInitMethod)

    # Assert
    assert [
        'attributeKey',
        'otherAttributeKey',
        'otherAttributeKeyAgain',
        'someOtherAttributeKey',
        'otherAttributeKeyOnceAgain'
    ] == myClassArgsOrder
    assert [] == myClassWithoutAttributesArgsOrder
    assert [
        'attributeKey'
    ] == myClassWithLessAttributesThanArgsArgsOrder
    assert [
        'attributeKey'
    ] == myClassWithMoreAttributesThanArgsArgsOrder
    assert [] == myClassWithoutInitMethodArgsOrder


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True,
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
    },
    **TEST_SETTINGS
)
def getAttributeOrMethodByNamePath():
    #arrange
    class MyClass :
        def __init__(self, value):
            self.myAttribute = value
    FINAL_VALUE = 3
    DEFAULT_VALUE = 7
    instance = MyClass(MyClass(MyClass(MyClass(3))))

    #act
    finalValueToAssert = ReflectionHelper.getAttributeOrMethodByNamePath(instance, 'myAttribute.myAttribute.myAttribute.myAttribute', muteLogs=False, default=None)

    mustBeNone = ReflectionHelper.getAttributeOrMethodByNamePath(instance, 'myAttribute.myAttribute.myAttribute.myAttribute.myAttribute', muteLogs=False, default=None)
    mustBeDefault = ReflectionHelper.getAttributeOrMethodByNamePath(instance, 'myAttribute.myAttribute.myAttribute.myAttribute.myAttribute', muteLogs=False, default=DEFAULT_VALUE)

    mustBeNoneByEndingOnDot = ReflectionHelper.getAttributeOrMethodByNamePath(instance, 'myAttribute.', muteLogs=False, default=None)
    mustBeDefaultByEndingOnDot = ReflectionHelper.getAttributeOrMethodByNamePath(instance, 'myAttribute.', muteLogs=False, default=DEFAULT_VALUE)

    mustBeNoneByStartingOnDot = ReflectionHelper.getAttributeOrMethodByNamePath(instance, '.myAttribute', muteLogs=False, default=None)
    mustBeDefaultByStartingOnDot = ReflectionHelper.getAttributeOrMethodByNamePath(instance, '.myAttribute', muteLogs=False, default=DEFAULT_VALUE)

    hereWeGo = ReflectionHelper.getAttributeOrMethodByNamePath(instance, 'myAttribute..myAttribute', muteLogs=False, default=None)
    hereWeGoDefault = ReflectionHelper.getAttributeOrMethodByNamePath(instance, 'myAttribute..myAttribute', muteLogs=False, default=DEFAULT_VALUE)

    #assert
    assert FINAL_VALUE == finalValueToAssert, f'{FINAL_VALUE} == {finalValueToAssert}'

    assert ObjectHelper.isNone(mustBeNone)
    assert DEFAULT_VALUE == mustBeDefault, f'{DEFAULT_VALUE} == {mustBeDefault}'

    assert ObjectHelper.isNone(mustBeNoneByEndingOnDot)
    assert DEFAULT_VALUE == mustBeDefaultByEndingOnDot

    assert ObjectHelper.isNone(mustBeNoneByStartingOnDot)
    assert DEFAULT_VALUE == mustBeDefaultByStartingOnDot

    assert ObjectHelper.isNone(hereWeGo)
    assert DEFAULT_VALUE == hereWeGoDefault

    assert ObjectHelper.isNotNone(instance.myAttribute.myAttribute)
    assert ObjectHelper.equals(instance.myAttribute.myAttribute, ReflectionHelper.getAttributeOrMethodByNamePath(instance, 'myAttribute.myAttribute', muteLogs=False, default=None))
    assert ObjectHelper.isNotNone(instance.myAttribute)
    assert not ObjectHelper.equals(instance.myAttribute, ReflectionHelper.getAttributeOrMethodByNamePath(instance, 'myAttribute.myAttribute', muteLogs=False, default=None))


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True,
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
    },
    **TEST_SETTINGS
)
def getName_manyCases() :
    # arrange
    def functionMine() :
        return None
    class Me:
        an = 2
        def __init__(self) :
            self.na = 'yey'
        def methodIsMine() :
            return True

    # act
    functionNameToAsert = ReflectionHelper.getName(functionMine)
    instanceNameToAsert = ReflectionHelper.getName(Me())
    classNameToAsert = ReflectionHelper.getName(Me)
    methodNameToAsert = ReflectionHelper.getName(Me().methodIsMine)
    attributeNameToAsert = ReflectionHelper.getName(Me().an)
    staticAttributeNameToAsert = ReflectionHelper.getName(Me().na)

    class_functionNameToAsert = ReflectionHelper.getClassName(functionMine)
    class_instanceNameToAsert = ReflectionHelper.getClassName(Me())
    class_classNameToAsert = ReflectionHelper.getClassName(Me)
    class_methodNameToAsert = ReflectionHelper.getClassName(Me().methodIsMine)
    class_attributeNameToAsert = ReflectionHelper.getClassName(Me().an)
    class_staticAttributeNameToAsert = ReflectionHelper.getClassName(Me().na)

    type_functionNameToAsert = ReflectionHelper.getName(type(functionMine))
    type_instanceNameToAsert = ReflectionHelper.getName(type(Me()))
    type_classNameToAsert = ReflectionHelper.getName(type(Me))
    type_methodNameToAsert = ReflectionHelper.getName(type(Me().methodIsMine))
    type_attributeNameToAsert = ReflectionHelper.getName(type(Me().an))
    type_staticAttributeNameToAsert = ReflectionHelper.getName(type(Me().na))

    type_class_functionNameToAsert = ReflectionHelper.getClassName(type(functionMine))
    type_class_instanceNameToAsert = ReflectionHelper.getClassName(type(Me()))
    type_class_classNameToAsert = ReflectionHelper.getClassName(type(Me))
    type_class_methodNameToAsert = ReflectionHelper.getClassName(type(Me().methodIsMine))
    type_class_attributeNameToAsert = ReflectionHelper.getClassName(type(Me().an))
    type_class_staticAttributeNameToAsert = ReflectionHelper.getClassName(type(Me().na))

    None_functionNameToAsert = ReflectionHelper.getName(None)
    None_instanceNameToAsert = ReflectionHelper.getName(None)
    None_classNameToAsert = ReflectionHelper.getName(None)
    None_methodNameToAsert = ReflectionHelper.getName(None)
    None_attributeNameToAsert = ReflectionHelper.getName(None)
    None_staticAttributeNameToAsert = ReflectionHelper.getName(None)

    None_class_functionNameToAsert = ReflectionHelper.getClassName(None)
    None_class_instanceNameToAsert = ReflectionHelper.getClassName(None)
    None_class_classNameToAsert = ReflectionHelper.getClassName(None)
    None_class_methodNameToAsert = ReflectionHelper.getClassName(None)
    None_class_attributeNameToAsert = ReflectionHelper.getClassName(None)
    None_class_staticAttributeNameToAsert = ReflectionHelper.getClassName(None)

    parent_functionNameToAsert = ReflectionHelper.getParentClass(functionMine)
    parent_instanceNameToAsert = ReflectionHelper.getParentClass(Me())
    parent_classNameToAsert = ReflectionHelper.getParentClass(Me)
    actual_parent_methodNameToAsert = Me()
    parent_methodNameToAsert = ReflectionHelper.getParentClass(actual_parent_methodNameToAsert.methodIsMine)
    parent_attributeNameToAsert = ReflectionHelper.getParentClass(Me().an)
    parent_staticAttributeNameToAsert = ReflectionHelper.getParentClass(Me().na)
    parent_testFunctionNameToAsert = ReflectionHelper.getParentClass(getName_manyCases)
    
    # assert
    assert 'functionMine' == functionNameToAsert
    assert '(undefined)' == instanceNameToAsert, f'(undefined) == {instanceNameToAsert}'
    assert 'Me' == classNameToAsert
    assert 'methodIsMine' == methodNameToAsert
    assert '(undefined)' == attributeNameToAsert
    assert '(undefined)' == staticAttributeNameToAsert

    assert 'function' == class_functionNameToAsert
    assert 'Me' == class_instanceNameToAsert
    assert 'Me' == class_classNameToAsert, class_classNameToAsert
    assert 'method' == class_methodNameToAsert
    assert 'int' == class_attributeNameToAsert
    assert 'str' == class_staticAttributeNameToAsert

    assert 'function' == type_functionNameToAsert
    assert 'Me' == type_instanceNameToAsert
    assert 'type' == type_classNameToAsert
    assert 'method' == type_methodNameToAsert
    assert 'int' == type_attributeNameToAsert
    assert 'str' == type_staticAttributeNameToAsert

    assert 'function' == type_class_functionNameToAsert, type_class_functionNameToAsert
    assert 'Me' == type_class_instanceNameToAsert, type_class_instanceNameToAsert
    assert 'type' == type_class_classNameToAsert, type_class_classNameToAsert
    assert 'method' == type_class_methodNameToAsert, type_class_methodNameToAsert
    assert 'int' == type_class_attributeNameToAsert, type_class_attributeNameToAsert
    assert 'str' == type_class_staticAttributeNameToAsert, type_class_staticAttributeNameToAsert

    assert '(undefined)' == None_functionNameToAsert
    assert '(undefined)' == None_instanceNameToAsert
    assert '(undefined)' == None_classNameToAsert
    assert '(undefined)' == None_methodNameToAsert
    assert '(undefined)' == None_attributeNameToAsert
    assert '(undefined)' == None_staticAttributeNameToAsert

    assert 'None' == None_class_functionNameToAsert
    assert 'None' == None_class_instanceNameToAsert
    assert 'None' == None_class_classNameToAsert
    assert 'None' == None_class_methodNameToAsert
    assert 'None' == None_class_attributeNameToAsert
    assert 'None' == None_class_staticAttributeNameToAsert

    assert None == parent_functionNameToAsert, parent_functionNameToAsert
    assert None == parent_instanceNameToAsert, parent_instanceNameToAsert
    assert None == parent_classNameToAsert, parent_classNameToAsert
    assert actual_parent_methodNameToAsert.__class__ == parent_methodNameToAsert, f'{actual_parent_methodNameToAsert} == {parent_methodNameToAsert}'
    assert None == parent_attributeNameToAsert, parent_attributeNameToAsert
    assert None == parent_staticAttributeNameToAsert, parent_staticAttributeNameToAsert
    assert parent_testFunctionNameToAsert == ReflectionHelper.getParentClass(getName_manyCases), f'{parent_testFunctionNameToAsert} == {ReflectionHelper.getName(getName_manyCases)}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True,
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
    },
    **TEST_SETTINGS
)
def getAttributeNameListFromInstance():
    #arrange
    MY_ATTRIBUTE_NAME = 'myAttribute'
    MY_OTHER_ATTRIBUTE_NAME = 'myOtherAttribute'
    class MyObject:
        def __init__(self, myAttribute, myOtherAttribute=None) :
            self.myAttribute = myAttribute
            self.myOtherAttribute = myOtherAttribute
        def myMethod(self):
            return self.myAttribute
    myObject = ReflectionHelper.instanciateItWithNoArgsConstructor(MyObject)

    #act
    attributeNameList = ReflectionHelper.getAttributeNameListFromInstance(myObject)

    #assert
    assert [MY_ATTRIBUTE_NAME, MY_OTHER_ATTRIBUTE_NAME] == attributeNameList


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True,
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
    },
    **TEST_SETTINGS
)
def getAttributeDataDictionary():
    #arrange
    class TestClass:
        testAttribute = 2
        def __init__(self, anoterTestAttribute):
            self.anoterTestAttribute = anoterTestAttribute
    anoterTestAttributeValue = 'yolo'
    expected = {
        'testAttribute': 2,
        'anoterTestAttribute': anoterTestAttributeValue
    }
    instante = TestClass(anoterTestAttributeValue)

    #act
    toAssert = ReflectionHelper.getAttributeDataDictionary(instante)

    #assert
    assert ObjectHelper.equals(expected, toAssert)


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True,
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
    },
    **TEST_SETTINGS
)
def isClass():
    #arrange
    def myFunction(l):
        return l

    class TestClass:
        testAttribute = 2
        def __init__(self, anoterTestAttribute):
            self.anoterTestAttribute = anoterTestAttribute

    #act & assert
    assert ReflectionHelper.isClass(TestClass)
    assert ObjectHelper.isNotNone(ReflectionHelper.isClass(TestClass('e')))
    assert not ReflectionHelper.isClass(TestClass('e'))

    assert ReflectionHelper.isClass(float)
    assert ObjectHelper.isNotNone(ReflectionHelper.isClass(1.1))
    assert not ReflectionHelper.isClass(1.1)

    assert ReflectionHelper.isClass(int)
    assert ObjectHelper.isNotNone(ReflectionHelper.isClass(1))
    assert not ReflectionHelper.isClass(1)

    assert ReflectionHelper.isClass(str)
    assert ObjectHelper.isNotNone(ReflectionHelper.isClass('1'))
    assert not ReflectionHelper.isClass('1')

    assert ReflectionHelper.isClass(list)
    assert ObjectHelper.isNotNone(ReflectionHelper.isClass([1]))
    assert not ReflectionHelper.isClass([1])

    assert ReflectionHelper.isClass(tuple)
    assert ObjectHelper.isNotNone(ReflectionHelper.isClass(tuple([1])))
    assert not ReflectionHelper.isClass(tuple([1]))

    assert ReflectionHelper.isClass(set)
    assert ObjectHelper.isNotNone(ReflectionHelper.isClass(set([1])))
    assert not ReflectionHelper.isClass(set([1]))

    assert ReflectionHelper.isClass(dict)
    assert ObjectHelper.isNotNone(ReflectionHelper.isClass({1:3}))
    assert not ReflectionHelper.isClass({1:3})

    assert ObjectHelper.isNotNone(ReflectionHelper.isClass(myFunction))
    assert not ReflectionHelper.isClass(myFunction)

    assert ObjectHelper.isNotNone(ReflectionHelper.isClass(range(1)))
    assert not ReflectionHelper.isClass(range(1))


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True,
        SettingHelper.ACTIVE_ENVIRONMENT : SettingHelper.LOCAL_ENVIRONMENT,
        **LOG_HELPER_SETTINGS
    },
    **TEST_SETTINGS
)
def getItNaked():
    #arrange
    A = 2
    def getA():
        B = A
        return B + 1
    F = getA()

    #act and assert
    print(ReflectionHelper.getCompleteInstanceNameList(A))
    print(ReflectionHelper.getCompleteInstanceNameList(F))

    print(ReflectionHelper.getInstanceNameList(A))
    print(ReflectionHelper.getInstanceNameList(F))

    log.debugIt(A)
    ReflectionHelper.getItNaked(A)
    log.debugIt(F)
    ReflectionHelper.getItNaked(F)



@Test()
def getCompleteInstanceNameList():
    #arange
    doo = []
    woo = doo
    foo = woo
    def local():
        bar = foo
        car = bar
        return ReflectionHelper.getCompleteInstanceNameList(car)
    expected = ['doo', 'woo', 'foo', 'bar', 'car', 'foo', '__inner_instance__ of class list: []']

    #act
    toAssert = local()

    #asser
    assert expected == toAssert, f'{expected} == {toAssert}'
    assert ['None'] == ReflectionHelper.getCompleteInstanceNameList(None), ReflectionHelper.getCompleteInstanceNameList(None)
    assert ['''__inner_instance__ of class set: <class 'set'>'''] == ReflectionHelper.getCompleteInstanceNameList(set), ReflectionHelper.getCompleteInstanceNameList(set)



@Test()
def getInstanceNameList():
    #arange
    doo = []
    woo = doo
    foo = woo
    def local():
        bar = foo
        car = bar
        return ReflectionHelper.getInstanceNameList(car)
    expected = ['doo', 'woo', 'foo', 'bar', 'car']

    #act
    toAssert = local()

    #asser
    assert expected == toAssert, f'{expected} == {toAssert}'
    assert ['expression or value of class None: None'] == ReflectionHelper.getInstanceNameList(None), ReflectionHelper.getInstanceNameList(None)
    assert ['''expression or value of class set: <class 'set'>'''] == ReflectionHelper.getInstanceNameList(set), ReflectionHelper.getInstanceNameList(set)



@Test()
def getInstanceName():
    #arange
    doo = []
    woo = doo
    foo = woo
    def local():
        bar = foo
        car = bar
        return ReflectionHelper.getInstanceName(car)
        #['doo', 'woo', 'foo', 'bar']
    expected = 'car'

    #act
    toAssert = local()

    #asser
    assert expected == toAssert, f'{expected} == {toAssert}'
    assert 'expression or value of class None: None' == ReflectionHelper.getInstanceName(None), ReflectionHelper.getInstanceName(None)
    assert f'expression or value of class set: {Constant.OPEN_SET}2{Constant.CLOSE_SET}' == ReflectionHelper.getInstanceName(set([2])), ReflectionHelper.getInstanceName(set([2]))



@Test()
def getInstanceName_whenExpression():
    #arange
    expected = '''expression or value of class list: ['my', 'elements']'''

    #act
    toAssert = ReflectionHelper.getInstanceName(['my', 'elements'])

    #asser
    assert expected == toAssert, f'{expected} == {toAssert}'