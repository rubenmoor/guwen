def search_form(request):
	from forms import SearchForm
	search_form = SearchForm()
	return {'search_form': search_form}