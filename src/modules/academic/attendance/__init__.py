# Module d'attendance - Point d'entrée principal
from .models import AttendanceModel, AttendanceStatsModel, AttendanceHistoryModel
from .controllers import AttendanceController, AttendanceStatsController, AttendanceHistoryController
from .services import AttendanceService
from .views import ModernAttendanceView

__all__ = [
    'AttendanceModel', 'AttendanceStatsModel', 'AttendanceHistoryModel',
    'AttendanceController', 'AttendanceStatsController', 'AttendanceHistoryController',
    'AttendanceService', 'ModernAttendanceView'
]
