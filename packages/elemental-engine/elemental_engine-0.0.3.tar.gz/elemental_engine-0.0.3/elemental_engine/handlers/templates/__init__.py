def render_template(template, language):
	return getattr(template, language)()



