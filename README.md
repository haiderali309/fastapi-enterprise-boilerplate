i will add contant latter


# How to use Logging in intire code base

You need to add this in the file where you need to add looging

-------->           from app.core.logging import logger 

Then you can use all this arrording to your need:

    logger.info()           ----> for natural / success log
    logger.warning()        ----> for warning in which app run but some wrong also exits log
    logger.error()          ----> for error log
    logger.exception()      ----> for unexpected behaviour
    logger.DEBUG()          ----> for debuging (dev enviornment)
    logger.CRITICAL()       ----> A very serious failure the application may stop working