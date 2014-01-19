def remove_splits(queryset):
	'''
	Build a second database where splits don't split,
	but dollar value continues to increase proportionally.
	'''
	return False

def filter_by_date(queryset, start, end):
	'''
	start and end dates are date tuples
	'''
	return queryset.objects.filter(date__range[str(start), str(end)])

def filter_by_date_len(queryset, start, length):
	'''
	start is a date tuple, length is a time-delta
	'''
	return querset.objects.filter(date__range[str(start), str(start + length)])

def filter_by_volume(queryset, mini, maxi):
	'''
	mini and maxi are trade volume...
	'''
	return queryset.objects.filter(volume__lt(maxi), volume__gt(mini))