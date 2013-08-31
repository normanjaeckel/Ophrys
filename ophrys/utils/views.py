from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, MonthArchiveView, FormView
from django.views.generic import CreateView as _CreateView, UpdateView as _UpdateView, DeleteView as _DeleteView


class ExtraFormFieldsMixin:
    """
    Mixin to add the functionality of extra form fields defined by the
    get_extra_form_fields() classmethod of the model to a create or update
    view.
    """
    def dispatch(self, *args, **kwargs):
        """
        Extra form fields are fetched.
        """
        try:
            self.extra_form_fields = self.model.get_extra_form_fields()
        except AttributeError:
            # There aren't any extra form fields.
            self.extra_form_fields = ()
        return super().dispatch(*args, **kwargs)

    def get_form(self, form_class):
        """
        Returns the form. Extra form fields are added if any exist.
        """
        form = super().get_form(form_class)
        for extra_form_field in self.extra_form_fields:
            form.fields[extra_form_field.get_name()] = extra_form_field.get_form_field()
        return form

    def get_initial(self):
        """
        Returns the intial values for the form. Initial values for extra form
        fields are added.
        """
        initial = super().get_initial()
        for extra_form_field in self.extra_form_fields:
            initial.update({extra_form_field.get_name(): extra_form_field.get_initial(instance=self.object)})
        return initial

    def form_valid(self, form):
        """
        Processes the valid form. The callbacks of extra form fields are
        processed too.
        """
        return_value = super().form_valid(form)
        for extra_form_field in self.extra_form_fields:
            extra_form_field.process_field(instance=self.object, value=form.cleaned_data[extra_form_field.get_name()])
        return return_value


class CreateView(ExtraFormFieldsMixin, _CreateView):
    """
    View to create objects. It contains the ExtraFormFieldsMixin.
    """


class UpdateView(ExtraFormFieldsMixin, _UpdateView):
    """
    View to update objects. It contains the ExtraFormFieldsMixin.
    """


class DeleteView(_DeleteView):
    """
    View to delete objects. You have to provide the argument 'success_url_name'
    instead of the argument 'success_url'.
    """
    def get_success_url(self):
        return reverse(self.success_url_name)
