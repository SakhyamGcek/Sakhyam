# views.py
from django.shortcuts import render, redirect
from .forms import MemberForm, MemberRoleForm
from .models import Member
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Member, MemberRole

def member_create(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MemberForm()
    return render(request, 'member_form.html', {'form': form})



def member_list(request):
    members = MemberRole.objects.all()
    
    # Categorize members into groups
    grouped_members = {}
    group_size = 4  # Number of members per group

    for index, member in enumerate(members):
        group_number = (index // group_size) + 1
        if group_number not in grouped_members:
            grouped_members[group_number] = []
        grouped_members[group_number].append(member)
    
    return render(request, 'member_list.html', {'grouped_members': grouped_members})
#return render(request, 'member_list.html', {'members': members})

# def thank_you(request):
#     return render(request, 'thank_you.html')


# def member_requests(request):
#     members = Member.objects.filter(is_approved=False)
#     return render(request, 'dashboard.html', {'members': members})

def approve_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.is_approved = True
    member.save()

    # Send email with PDF
    email_subject = 'Club Membership Approved'
    email_body = render_to_string('membership_approved_email.html', {'member': member})
    email = EmailMessage(
        email_subject,
        email_body,
        'sakhyam4@gmail.com',
        [member.email],
    )
    
    # Generate PDF
    pdf = generate_pdf('membership_certificate.html', {'member': member})
    email.attach('membership_certificate.pdf', pdf, 'application/pdf')
    email.send()

    return redirect('accounts:dashboard')

def generate_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    pdf = pisa.pisaDocument(html.encode("ISO-8859-1"), result)
    if not pdf.err:
        return result.getvalue()
    return None

def assign_role(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        role_form = MemberRoleForm(request.POST)
        if role_form.is_valid():
            # Save the role and associate it with the member
            member_role = role_form.save(commit=False)
            member_role.member = member
            member_role.save()

            # Optionally: Send confirmation email or perform other actions

            return redirect('accounts:dashboard')
    else:
        role_form = MemberRoleForm()

    return render(request, 'assign_role.html', {'member': member, 'role_form': role_form})


def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('accounts:dashboard')