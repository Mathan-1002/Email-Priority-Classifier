from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from . import ml
from .forms import EmailForm
from .models import Email


def index(request):
    form = EmailForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.save(commit=False)
        email.priority, email.confidence = ml.predict(email.subject, email.body)
        email.save()
        return redirect("index")

    level = request.GET.get("priority")
    emails = Email.objects.all()
    if level in dict(Email.PRIORITIES):
        emails = emails.filter(priority=level)
    counts = {p: Email.objects.filter(priority=p).count() for p, _ in Email.PRIORITIES}
    return render(request, "classifier/index.html", {
        "form": form, "emails": emails, "counts": counts, "level": level,
    })


@require_POST
def relabel(request, pk):
    email = get_object_or_404(Email, pk=pk)
    new = request.POST.get("priority")
    if new in dict(Email.PRIORITIES):
        email.priority, email.corrected, email.confidence = new, True, 1.0
        email.save()
    return redirect(request.META.get("HTTP_REFERER", "index"))


@require_POST
def delete(request, pk):
    get_object_or_404(Email, pk=pk).delete()
    return redirect("index")


@require_POST
def retrain(request):
    extra = [(ml._text(e.subject, e.body), e.priority) for e in Email.objects.filter(corrected=True)]
    ml.train(extra)
    return redirect("index")

