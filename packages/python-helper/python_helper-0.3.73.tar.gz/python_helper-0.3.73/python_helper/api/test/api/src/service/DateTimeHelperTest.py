import time, datetime
from python_helper import EnvironmentHelper, SettingHelper, ObjectHelper, log, Test, DateTimeHelper

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
    log.WARNING : False,
    log.WRAPPER : False,
    log.FAILURE : False,
    log.ERROR : False,
    log.TEST : False
}

TEST_SETTINGS = {}

@Test()
def timeDelta() :
    # arrange
    # act
    # assert
    assert datetime.timedelta(days=2, hours=3, minutes=4, seconds=5, milliseconds=6, microseconds=7) == DateTimeHelper.timeDelta(days=2, hours=3, minutes=4, seconds=5, milliseconds=6, microseconds=7)
    assert datetime.timedelta(days=0, hours=3, minutes=4, seconds=5, milliseconds=6, microseconds=7) == DateTimeHelper.timeDelta(days=0, hours=3, minutes=4, seconds=5, milliseconds=6, microseconds=7)

# @Test()
# def dateTime_utcnow() :
#     # arrange
#     givenSimpleDateTime = time.time()
#     givenDateTime = date=datetime.datetime.utcnow()
#     givenDate = date=datetime.datetime.utcnow().date()
#     givenTime = date=datetime.datetime.utcnow().time()
#
#     # act
#     # assert
#     assert datetime.datetime.utcnow() == DateTimeHelper.dateTimeNow()
#     assert datetime.datetime.utcnow().date() == DateTimeHelper.dateOf(datetime.datetime.utcnow())
#     assert datetime.datetime.utcnow().time() == DateTimeHelper.timeOf(datetime.datetime.utcnow())
#     assert datetime.datetime.utcnow().date() == DateTimeHelper.dateNow()
#     assert datetime.datetime.utcnow().time() == DateTimeHelper.timeNow()
#     assert datetime.datetime.timestamp(datetime.datetime.utcnow()) == DateTimeHelper.timestampNow()
#     assert datetime.datetime.fromtimestamp(givenSimpleDateTime) == DateTimeHelper.ofTimestamp(givenSimpleDateTime)
#     assert datetime.datetime.utcnow() == DateTimeHelper.ofTimestamp(datetime.datetime.timestamp(DateTimeHelper.dateTimeNow()))
#
#     parsed = None
#     for pattern in DateTimeHelper.PATTERNS :
#         try :
#             parsed = datetime.datetime.strptime(str(givenDateTime), pattern)
#             break
#         except Exception as exception :
#             pass
#     assert parsed == DateTimeHelper.of(dateTime=givenDateTime)
#
#     parsed = None
#     for pattern in DateTimeHelper.PATTERNS :
#         try :
#             parsed = datetime.datetime.strptime(str(givenDate), pattern)
#             break
#         except Exception as exception :
#             pass
#     assert parsed == DateTimeHelper.of(date=givenDate)
#
#     parsed = None
#     for pattern in DateTimeHelper.PATTERNS :
#         try :
#             parsed = datetime.datetime.strptime(f'{datetime.datetime.utcnow().date()} {str(givenTime)}', pattern)
#             break
#         except Exception as exception :
#             pass
#     assert parsed == DateTimeHelper.of(time=givenTime), (parsed, DateTimeHelper.of(time=givenTime))
#
#     assert datetime.datetime.timestamp(givenDateTime) == DateTimeHelper.timestampOf(dateTime=givenDateTime), (datetime.datetime.timestamp(givenDateTime), DateTimeHelper.timestampOf(dateTime=givenDateTime))

@Test()
def dateTime_now() :
    # arrange
    givenDateTimeNow = datetime.datetime.now()
    timestampFromDatetimeNow = datetime.datetime.timestamp(datetime.datetime.now())
    givenSimpleDateTime = time.time()
    givenDateTime = datetime.datetime.now()
    givenDate = datetime.datetime.now().date()
    givenTime = datetime.datetime.now().time()
    givenTimeStampNow = DateTimeHelper.ofTimestamp(datetime.datetime.timestamp(DateTimeHelper.dateTimeNow()))
    margin = 550

    # act
    # assert
    assert (DateTimeHelper.dateTimeNow() - givenDateTimeNow).microseconds < margin, f'datetime.datetime.now() == DateTimeHelper.dateTimeNow() => {datetime.datetime.now()} == {DateTimeHelper.dateTimeNow()}'
    assert datetime.datetime.now().date() == DateTimeHelper.dateOf(datetime.datetime.now()), f'datetime.datetime.now().date() == DateTimeHelper.dateOf(datetime.datetime.now()) => {datetime.datetime.now().date()} == {DateTimeHelper.dateOf(datetime.datetime.now())}'
    assert abs(
        (
            datetime.datetime.now().time().second * 60000 + datetime.datetime.now().time().microsecond
        ) - (
            DateTimeHelper.timeNow().second * 60000 + DateTimeHelper.timeOf(datetime.datetime.now()).microsecond
        )
    ) < margin, f'datetime.datetime.now().time() == DateTimeHelper.timeOf(datetime.datetime.now()) => {datetime.datetime.now().time()} == {DateTimeHelper.timeOf(datetime.datetime.now())}'
    assert datetime.datetime.now().date() == DateTimeHelper.dateNow(), f'datetime.datetime.now().date() == DateTimeHelper.dateNow() => {datetime.datetime.now().date()} == {DateTimeHelper.dateNow()}'
    assert abs(
        (
            datetime.datetime.now().time().second * 60000 + datetime.datetime.now().time().microsecond
        ) - (
            DateTimeHelper.timeNow().second * 60000 + DateTimeHelper.timeNow().microsecond
        )
    ) < margin, f'datetime.datetime.now().time() == DateTimeHelper.timeNow() => {datetime.datetime.now().time()} == {DateTimeHelper.timeNow()}'
    assert DateTimeHelper.timestampNow() - timestampFromDatetimeNow < margin, f'datetime.datetime.timestamp(datetime.datetime.now()) == DateTimeHelper.timestampNow() => {datetime.datetime.timestamp(datetime.datetime.now())} == {DateTimeHelper.timestampNow()}'
    assert datetime.datetime.fromtimestamp(givenSimpleDateTime) == DateTimeHelper.ofTimestamp(givenSimpleDateTime), f'datetime.datetime.fromtimestamp(givenSimpleDateTime) == DateTimeHelper.ofTimestamp(givenSimpleDateTime) => {datetime.datetime.fromtimestamp(givenSimpleDateTime)} == {DateTimeHelper.ofTimestamp(givenSimpleDateTime)}'
    assert (givenTimeStampNow - givenDateTimeNow).microseconds < margin, f'datetime.datetime.now() == DateTimeHelper.ofTimestamp(datetime.datetime.timestamp(DateTimeHelper.dateTimeNow())) => {givenTimeStampNow} == {givenDateTimeNow}'

    parsed = None
    for pattern in DateTimeHelper.PATTERNS :
        try :
            parsed = datetime.datetime.strptime(str(givenDateTime), pattern)
            break
        except Exception as exception :
            pass
    assert parsed == DateTimeHelper.of(dateTime=givenDateTime)

    parsed = None
    for pattern in DateTimeHelper.PATTERNS :
        try :
            parsed = datetime.datetime.strptime(str(givenDate), pattern)
            break
        except Exception as exception :
            pass
    assert parsed == DateTimeHelper.of(date=givenDate)

    parsed = None
    for pattern in DateTimeHelper.PATTERNS :
        try :
            parsed = datetime.datetime.strptime(f'{datetime.datetime.now().date()} {str(givenTime)}', pattern)
            break
        except Exception as exception :
            pass
    assert parsed == DateTimeHelper.of(time=givenTime), (parsed, DateTimeHelper.of(time=givenTime))

    assert datetime.datetime.timestamp(givenDateTime) == DateTimeHelper.timestampOf(dateTime=givenDateTime), (datetime.datetime.timestamp(givenDateTime), DateTimeHelper.timestampOf(dateTime=givenDateTime))

@Test()
def getWeekDay() :
    # arrange
    dateTimeNow = datetime.datetime.now()
    timeNow = datetime.datetime.now().time()
    dateNow = datetime.datetime.now().date()

    # act
    # assert
    assert datetime.datetime.now().weekday() == DateTimeHelper.getWeekDay()
    assert datetime.datetime.now().weekday() == DateTimeHelper.getWeekDay(dateTime=dateTimeNow)
    assert datetime.datetime.now().weekday() == DateTimeHelper.getWeekDay(date=dateNow, time=timeNow)
    assert datetime.datetime.now().weekday() == DateTimeHelper.getWeekDay(date=dateNow)

@Test()
def plusMonths() :
    # arrange
    # act
    # assert
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=1
    ) == DateTimeHelper.of(dateTime = '2022-10-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 1 month == 2022-10-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=2
    ) == DateTimeHelper.of(dateTime = '2022-11-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 2 month == 2022-11-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=3
    ) == DateTimeHelper.of(dateTime = '2022-12-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 3 month == 2022-12-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=4
    ) == DateTimeHelper.of(dateTime = '2023-01-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 4 month == 2023-01-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=5
    ) == DateTimeHelper.of(dateTime = '2023-02-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 5 month == 2023-02-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=6
    ) == DateTimeHelper.of(dateTime = '2023-03-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 6 month == 2023-03-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=7
    ) == DateTimeHelper.of(dateTime = '2023-04-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 7 month == 2023-04-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=8
    ) == DateTimeHelper.of(dateTime = '2023-05-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 8 month == 2023-05-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=9
    ) == DateTimeHelper.of(dateTime = '2023-06-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 9 month == 2023-06-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=10
    ) == DateTimeHelper.of(dateTime = '2023-07-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 10 month == 2023-07-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=11
    ) == DateTimeHelper.of(dateTime = '2023-08-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 11 month == 2023-08-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=12
    ) == DateTimeHelper.of(dateTime = '2023-09-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 12 month == 2023-09-10 10:10:10.999'


    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-12-10 10:10:10.999'),
        months=0
    ) == DateTimeHelper.of(dateTime = '2022-12-10 10:10:10.999'), f'2022-12-10 10:10:10.999 + 0 month == 2022-12-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2022-12-10 10:10:10.999'),
        months=1
    ) == DateTimeHelper.of(dateTime = '2023-01-10 10:10:10.999'), f'2022-12-10 10:10:10.999 + 1 month == 2023-01-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2023-01-10 10:10:10.999'),
        months=0
    ) == DateTimeHelper.of(dateTime = '2023-01-10 10:10:10.999'), f'2023-01-10 10:10:10.999 + 0 month == 2023-01-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2023-01-10 10:10:10.999'),
        months=1
    ) == DateTimeHelper.of(dateTime = '2023-02-10 10:10:10.999'), f'2023-01-10 10:10:10.999 + 1 month == 2023-02-10 10:10:10.999'
    assert DateTimeHelper.plusMonths(
        DateTimeHelper.of(dateTime = '2023-03-10 10:10:10.999'),
        months=34
    ) == DateTimeHelper.of(dateTime = '2026-01-10 10:10:10.999'), f'2023-03-10 10:10:10.999 + 34 month == 2026-01-10 10:10:10.999: {DateTimeHelper.plusMonths(DateTimeHelper.of(dateTime = "2023-03-10 10:10:10.999"), months=34)}'

@Test()
def minusMonths() :
    # arrange
    # act
    # assert
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=1
    ) == DateTimeHelper.of(dateTime = '2022-08-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 1 month == 2022-08-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=2
    ) == DateTimeHelper.of(dateTime = '2022-07-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 2 month == 2022-07-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=3
    ) == DateTimeHelper.of(dateTime = '2022-06-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 3 month == 2022-06-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=4
    ) == DateTimeHelper.of(dateTime = '2022-05-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 4 month == 2022-05-10 10:10:10.999: {DateTimeHelper.minusMonths(DateTimeHelper.of(dateTime = "2022-09-10 10:10:10.999"), months=4)}'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=5
    ) == DateTimeHelper.of(dateTime = '2022-04-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 5 month == 2022-04-10 10:10:10.999: {DateTimeHelper.minusMonths(DateTimeHelper.of(dateTime = "2022-09-10 10:10:10.999"), months=5)}'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=6
    ) == DateTimeHelper.of(dateTime = '2022-03-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 6 month == 2022-03-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=7
    ) == DateTimeHelper.of(dateTime = '2022-02-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 7 month == 2022-02-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=8
    ) == DateTimeHelper.of(dateTime = '2022-01-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 8 month == 2022-01-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=9
    ) == DateTimeHelper.of(dateTime = '2021-12-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 9 month == 2021-12-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=10
    ) == DateTimeHelper.of(dateTime = '2021-11-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 10 month == 2021-11-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=11
    ) == DateTimeHelper.of(dateTime = '2021-10-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 11 month == 2021-10-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=12
    ) == DateTimeHelper.of(dateTime = '2021-09-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 12 month == 2021-09-10 10:10:10.999'


    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-02-10 10:10:10.999'),
        months=0
    ) == DateTimeHelper.of(dateTime = '2022-02-10 10:10:10.999'), f'2022-02-10 10:10:10.999 - 0 month == 2022-02-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-02-10 10:10:10.999'),
        months=1
    ) == DateTimeHelper.of(dateTime = '2022-01-10 10:10:10.999'), f'2022-02-10 10:10:10.999 - 0 month == 2022-01-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-01-10 10:10:10.999'),
        months=0
    ) == DateTimeHelper.of(dateTime = '2022-01-10 10:10:10.999'), f'2022-01-10 10:10:10.999 - 0 month == 2022-01-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-01-10 10:10:10.999'),
        months=1
    ) == DateTimeHelper.of(dateTime = '2021-12-10 10:10:10.999'), f'2022-01-10 10:10:10.999 - 1 month == 2021-12-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-12-10 10:10:10.999'),
        months=0
    ) == DateTimeHelper.of(dateTime = '2022-12-10 10:10:10.999'), f'2022-12-10 10:10:10.999 - 0 month == 2022-12-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-12-10 10:10:10.999'),
        months=1
    ) == DateTimeHelper.of(dateTime = '2022-11-10 10:10:10.999'), f'2022-12-10 10:10:10.999 - 1 month == 2022-11-10 10:10:10.999'

    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=14
    ) == DateTimeHelper.of(dateTime = '2021-07-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 14 month == 2021-07-10 10:10:10.999'
    assert DateTimeHelper.minusMonths(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        months=34
    ) == DateTimeHelper.of(dateTime = '2019-11-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 34 month == 2019-11-10 10:10:10.999'


@Test()
def minusMonth_when31July() :
    #arrange, act and assert
    assert '2023-06-30 00:00:00' == str(DateTimeHelper.minusMonths(DateTimeHelper.of(date='2023-07-31'), months=1)), '2023-06-30' + ' == ' + str(DateTimeHelper.minusMonths(DateTimeHelper.of(date='2023-07-31'), months=1))


@Test()
def plusYears() :
    # arrange
    # act
    # assert
    assert DateTimeHelper.plusYears(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        years=1
    ) == DateTimeHelper.of(dateTime = '2023-09-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 1 year == 2023-09-10 10:10:10.999'
    assert DateTimeHelper.plusYears(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        years=2
    ) == DateTimeHelper.of(dateTime = '2024-09-10 10:10:10.999'), f'2022-09-10 10:10:10.999 + 2 year == 2024-09-10 10:10:10.999'
    

@Test()
def minusYears() :
    # arrange
    # act
    # assert
    assert DateTimeHelper.minusYears(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        years=1
    ) == DateTimeHelper.of(dateTime = '2021-09-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 1 year == 2021-09-10 10:10:10.999'
    assert DateTimeHelper.minusYears(
        DateTimeHelper.of(dateTime = '2022-09-10 10:10:10.999'),
        years=2
    ) == DateTimeHelper.of(dateTime = '2020-09-10 10:10:10.999'), f'2022-09-10 10:10:10.999 - 2 year == 2020-09-10 10:10:10.999'


@Test()
def isNativeDateTime():
    #arrange
    isDateTimeAsString = '2022-09-10 10:10:10.999'
    isDateAsDateTime = DateTimeHelper.of(isDateTimeAsString)

    #act
    isDateTimeAsStringToAssert = DateTimeHelper.isNativeDateTime(isDateTimeAsString)
    isDateAsDateTimeToAssert = DateTimeHelper.isNativeDateTime(isDateAsDateTime)

    #assert
    assert not isDateTimeAsStringToAssert
    assert isDateAsDateTimeToAssert
    assert not DateTimeHelper.isNativeDateTime('2020-02-10 10:09:10.999')
    assert DateTimeHelper.isNativeDateTime(DateTimeHelper.of('2020-02-10 10:09:10.999'))
    assert False == DateTimeHelper.isNativeDateTime('abcd'), 'abcd is not date time'
    assert False == DateTimeHelper.isNativeDateTime(None), f'{None} is not date time'
    assert False == DateTimeHelper.isNativeDateTime((1,)), f'{(1,)} is not date time'
    assert False == DateTimeHelper.isNativeDateTime(list()), f'{list()} is not date time'
    assert False == DateTimeHelper.isNativeDateTime(set()), f'{set()} is not date time'
    assert False == DateTimeHelper.isNativeDateTime(dict()), f'{dict()} is not date time'
    assert False == DateTimeHelper.isNativeDateTime(1), f'{1} is not date time'
    assert False == DateTimeHelper.isNativeDateTime(1.0), f'{1.0} is not date time'
    assert False == DateTimeHelper.isNativeDateTime(True), f'{True} is not date time'
    assert False == DateTimeHelper.isNativeDateTime(False), f'{False} is not date time'


@Test()
def isDateTime():
    #arrange
    isDateTimeAsString = '2022-09-10 10:10:10.999'
    isDateAsDateTime = DateTimeHelper.of(isDateTimeAsString)

    #act
    isDateTimeAsStringToAssert = DateTimeHelper.isDateTime(isDateTimeAsString)
    isDateAsDateTimeToAssert = DateTimeHelper.isDateTime(isDateAsDateTime)

    #assert
    assert True == isDateTimeAsStringToAssert
    assert True == isDateAsDateTimeToAssert
    assert DateTimeHelper.isDateTime('2020-02-10 10:09:10.999')
    assert DateTimeHelper.isDateTime(DateTimeHelper.of('2020-02-10 10:09:10.999'))
    assert False == DateTimeHelper.isDateTime('abcd'), 'abcd is not date time'
    assert False == DateTimeHelper.isDateTime(None), f'{None} is not date time'
    assert False == DateTimeHelper.isDateTime((1,)), f'{(1,)} is not date time'
    assert False == DateTimeHelper.isDateTime(list()), f'{list()} is not date time'
    assert False == DateTimeHelper.isDateTime(set()), f'{set()} is not date time'
    assert False == DateTimeHelper.isDateTime(dict()), f'{dict()} is not date time'
    assert False == DateTimeHelper.isDateTime(1), f'{1} is not date time'
    assert False == DateTimeHelper.isDateTime(1.0), f'{1.0} is not date time'
    assert False == DateTimeHelper.isDateTime(True), f'{True} is not date time'
    assert False == DateTimeHelper.isDateTime(False), f'{False} is not date time'


@Test()
def plusMonths_when_2023_01_31():
    #arrange
    dateTimeAsString = DateTimeHelper.of('2023-01-31 10:10:10.999')
    expected = DateTimeHelper.of('2023-02-28 10:10:10.999')

    #act
    toAssert = DateTimeHelper.plusMonths(dateTimeAsString, months=1)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'