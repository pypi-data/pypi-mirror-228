from odoo import api, fields, models, _
from datetime import timedelta
from pytz import timezone
from logging import getLogger
_logger = getLogger(__name__)


class HrAttendanceMitxelena(models.Model):
    _inherit = 'hr.attendance'
    is_holiday = fields.Boolean(compute='_compute_is_holiday', store=True)
    is_relevo = fields.Boolean(string='Relevo', compute='_compute_is_relevo', store=True)
    shift_type = fields.Selection([
        ('', _('Unknown')),
        ('morning', _('Morning')),
        ('afternoon', _('Afternoon')),
        ('night', _('Night')),
    ], compute='_compute_shift_type', store=True)

    entry_type = fields.Char(compute='_compute_entry_type', store=True)

    consecutive_days = fields.Integer(
        compute='_compute_consecutive_days', store=True, default=1)
    
    def _compute_entry_type(self):
        if self.is_holiday:
            return 'holiday'
        if self.count_as_weekend():
            return 'weekend'
        if self.is_relevo and self.shift_type != 'night':
            return 'relevo'
        elif self.is_relevo and self.shift_type == 'night':   
            return 'relevo night'
        else:
            return 'not computed'

    def count_as_weekend(self):
        # Get user timezone, or use Europe/Madrid as default
        tz = timezone(self.env.user.tz or 'Europe/Madrid')
        self.ensure_one()
        check_in = self.check_in.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
        # if is holiday, is not weekend
        if self.is_holiday:
            return False
        # if check_in is in Sunday but shift_type is night, is not weekend
        if check_in.weekday() == 6 and self.shift_type == 'night':
            return False
        # if check_in is between Monday and Friday, is not weekend
        if check_in.weekday() < 5:
            return False        
        return True
    
    @api.depends('check_in', 'consecutive_days')
    def _compute_is_relevo(self):
        self.ensure_one()

        is_relevo = False        
        tz = timezone(self.env.user.tz or 'Europe/Madrid')
        check_in = self.check_in.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)

        # if consecutive_days is bigger than 5, is not relevo
        if self.consecutive_days > 5:
            return False
        
        # if is holiday, is not relevo
        if self.is_holiday:
            return False

        # if check_in is between Monday and Friday, is relevo
        if check_in.weekday() < 5:
            is_relevo = True

        #  if check_in is in Sunday but shift_type is night, is relevo        
        if check_in.weekday() == 6 and self.shift_type == 'night':
            is_relevo = True

        return is_relevo

    @api.depends('check_in')
    def _compute_is_holiday(self):
        holiday_model = self.env['hr.holidays.public']
        for record in self:
            if record.check_in:
                # Check if the check_in date is a public holiday
                record.is_holiday = holiday_model.is_public_holiday(
                    record.check_in.date())
            else:
                # If there is no check_in, we can't compute if it's a holiday
                record.is_holiday = False

    @api.depends('check_out')
    def _compute_shift_type(self):
        # Get user timezone, or use Europe/Madrid as default
        tz = timezone(self.env.user.tz or 'Europe/Madrid')
        for record in self:
            if record.check_in and record.check_out:
                # Convert check_in and check_out to local time
                check_in = record.check_in.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                check_out = record.check_out.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                midpoint = check_in + (check_out - check_in) / 2
                hour = midpoint.hour
                if 5 <= hour < 13:
                    shift_type = 'morning'
                elif 13 <= hour < 21:
                    shift_type = 'afternoon'
                else:
                    shift_type = 'night'
                record.shift_type = shift_type

    @api.depends('check_in', 'shift_type', 'worked_hours')
    def _compute_consecutive_days(self):
        
        self.ensure_one()
        # If there is no check_in, set consecutive days to 0
        # and break the loop
        if not self.check_in:
            self.consecutive_days = 0
            return self.consecutive_days

        # Get the last 7 days range
        datetime_end = self.check_in
        datetime_start = datetime_end - timedelta(days=6)

        # Only select attendances where worked_hours > 0.5 hours
        # to avoid erroneous short attendances
        attendance_records = self.env['hr.attendance'].search([
            ('employee_id', '=', self.employee_id.id),
            ('check_in', '>=', datetime_start),
            ('check_in', '<=', datetime_end),
            ('worked_hours', '>', 0.5)
        ], order='check_in desc')

        # Init inner-loop variables
        previous_record = None
        consecutive_days = 1
        _logger.debug('[%s][%i][Init] Counting consecutive days',
                        self.id, consecutive_days)

        # If there are no attendance records, set consecutive days to 1
        # and break the loop
        if len(attendance_records) == 0:
            self.consecutive_days = 1
            _logger.debug('[%s][%i] No previous attendance records found',
                            self.id, consecutive_days)
            return consecutive_days

        # Iterate over the past attendance records
        for rec in attendance_records:
            _logger.debug(
                '[%s] Checking past attendance %s', self.id, rec)

            # If there is no previous record, set it to the current one
            # and continue the loop
            if not previous_record:
                previous_record = rec
                _logger.debug(
                    '[%s] No previous record found, setting %s',
                    self.id, rec)
                continue

            check_in_date = rec.check_in.date()
            previous_check_in_date = previous_record.check_in.date()

            # If the previous record it's not within the last day
            # break the loop and stop counting consecutive days
            is_consecutive = (previous_check_in_date -
                                check_in_date) <= timedelta(days=1)

            if not is_consecutive:
                _logger.debug(
                        '[%s] Records are not consecutive (%s)',
                        self.id, rec.id)
                break

            # If the previous record it is not the same day,
            # add a consecutive day and continue the loop
            if previous_check_in_date != check_in_date:
                consecutive_days += 1
                _logger.debug('[%s] +1 consecutive days: %i',
                                self.id, consecutive_days)
                previous_record = rec
                continue
                
            # If the previous record has less than 2 hours worked,
            # skip this record and continue the loop                    
            if rec.worked_hours < 2:
                _logger.debug(
                    '[%s] Same day, but less than 2 hours worked (%s)',
                    self.id, rec.id)                    
                previous_record = rec
                continue

            time_difference = previous_record.check_in - rec.check_out
            
            # If the previous record it's more than 7 hours
            # from the current one, add a consecutive day
            if (time_difference >= timedelta(hours=7)):                        
                _logger.debug(
                    '[%s] Same day, but more than 7 hours difference',
                    self.id)
                
                consecutive_days += 1

                _logger.debug(
                    '[%s] so, +1 consecutive days: %i', self.id, 
                    consecutive_days)
                            
                # Set the previous record to the current one
                previous_record = rec

        # Set the final consecutive days count to the record
        self.consecutive_days = consecutive_days

        _logger.debug('[%s][%i][Final] Consecutive days for %s has ended.',
                self.id, consecutive_days, self.employee_id.name)

    def recompute_all(self):
        # Get all records  from hr.attendance and iterate over them
        attendance_records = self.env['hr.attendance'].search([])
        _logger.debug('Attendance records: %s', attendance_records)
        for record in attendance_records:
            _logger.debug('Updating is_holiday for %s', record)
            record.is_holiday = record._compute_is_holiday()
            _logger.debug('Is holiday: %s', record.is_holiday)
            record.shift_type = record._compute_shift_type()
            _logger.debug('Shift type: %s', record.shift_type)

    def recompute_shifts(self):
        tz = timezone(self.env.user.tz or 'Europe/Madrid')
        attendance_records = self.env['hr.attendance'].search([])
        _logger.debug('Attendance records: %s', attendance_records)
        for record in attendance_records:
            try:
                check_in = record.check_in.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                check_out = record.check_out.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                midpoint = check_in + (check_out - check_in) / 2
                hour = midpoint.hour
                if 5 <= hour < 13:
                    shift_type = 'morning'
                elif 13 <= hour < 21:
                    shift_type = 'afternoon'
                else:
                    shift_type = 'night'
                record.shift_type = shift_type
                _logger.debug('Shift type %s for %s', shift_type, record)
                if record.shift_type != shift_type:
                    _logger.error('Shift type is %s for %s',
                                  record.shift_type, record)
                record._compute_consecutive_days()
            except Exception as e:
                _logger.error(
                    'Error computing shift type for %s: %s', record, e)
