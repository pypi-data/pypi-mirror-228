### installation
* Add `django-mp-modal` to `requirements.txt`
* Add `modal` to `INSTALLED_APPS`
* Add `js/Modal.js` to js files

View example:
```
class CreateCallbackView(ModalFormView):

    form_class = MyFormClass
    template_name = 'myapp/modal.html'

    def get_success_context(self, obj):
        return {
            "message": _('Success')
        }
```

Also, it's possible to rewrite:
* `save_form(self, form)` method
* `get_initial(self)` method

Html example:
```

{% extends "modal.html" %}

{% load i18n widget_tweaks %}


{% block title %}
	{% trans 'My Form' %}
{% endblock %}


{% block body %}
	<form method="post">
        {% csrf_token %}

        <div class="form-group m-b-10 {% if form.mobile.errors %}has-error{% endif %}">
            {{ form.mobile.label_tag }}
            {{ form.mobile|add_class:"form-control input-lg" }}
            {% if form.mobile.errors %}
                <span class="help-block">{{ form.mobile.errors }}</span>
            {% endif %}
        </div>
        <div class="form-group">
            {{ form.captcha }}
            {% if form.captcha.errors %}
                <p class="text-danger">{{ form.captcha.errors.as_text }}</p>
            {% endif %}
        </div>
    </form>
{% endblock %}


{% block footer %}
	<button type="button" class="btn btn-success pull-left" data-role="submit-btn">
        {% trans 'Save' %}
    </button>

    <button type="button" class="btn btn-default" data-dismiss="modal">
        {% trans 'Cancel' %}
    </button>
{% endblock %}
```
