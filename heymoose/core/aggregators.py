from heymoose.utils import times
import actions.shows as shows
import actions.actions as actions


class Aggregator(object):
	def aggregate(self):
		pass


class ShowsAndClicksAggregator(Aggregator):
	config = dict(
		minute = dict(
			format=lambda d: d.strftime('%d.%m.%y') if d.hour == 0 and d.minute == 0 else d.strftime('%H:%M'), 
			freq=times.MINUTELY,
			fbegin=times.begin_of_minute,
			fend=times.end_of_minute),
		hour = dict(
			format=lambda d: d.strftime('%d.%m.%y') if d.hour == 0 and d.minute == 0 else d.strftime('%H:00'),
			freq=times.HOURLY,
			fbegin=times.begin_of_hour,
			fend=times.end_of_hour),
		day = dict(
			format=lambda d: d.strftime('%d.%m.%y'),
			freq=times.DAILY,
			fbegin=times.begin_of_day,
			fend=times.end_of_day),
		month = dict(
			format=lambda d: d.strftime('%m.%y'),
			freq=times.MONTHLY,
			fbegin=times.begin_of_month,
			fend=times.end_of_month)
	)
	
	def __init__(self, fm, to, group, **kwargs):
		self.fm = fm
		self.to = to
		self.group = group
		self.kwargs = kwargs
		
	def aggregate(self):
		conf = self.config.get(self.group)
		format = conf.get('format')	# Current datetime formatting function
		freq = conf.get('freq')		# Current frequency
		fbegin = conf.get('fbegin')	# Converter to begin of period
		fend = conf.get('fend')		# Converter to end of period
		
		# Align entered datetimes by current group
		dtbegin = fbegin(self.fm)
		dtend = fend(self.to)
		
		# Generate some test random data
		#checkpoints = times.datetime_range(times.MINUTELY, dtstart=dtbegin, until=dtend)
		#clicks = [random.choice(checkpoints) for _x in range(10)]
		#shows = [random.choice(checkpoints) for _x in range(10000)]
		
		# But this is real data from backend
		acts = actions.get_actions_range(dtbegin, dtend, **self.kwargs)
		shws = shows.get_shows_range(dtbegin, dtend, **self.kwargs)
		
		# List of all times in interval with period depending on group
		keys = times.datetime_range(freq, dtstart=dtbegin, until=dtend)
		
		# Fill result dict with test data
		result = dict([(key, [0, 0]) for key in keys])
		for act in acts: result[fbegin(act.creation_time)][0] += 1
		for shw in shws: result[fbegin(shw.show_time)][1] += 1
		
		# This magic expression transforms dict to list of dicts sorted by datetime	
		return [dict(time=format(key), clicks=value[0], shows=value[1]) \
				for key, value in sorted(result.items(), key=lambda item: item[0])]
		
		
		
		