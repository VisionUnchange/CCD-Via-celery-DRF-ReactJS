from django.utils.safestring import mark_safe

from wagtail.wagtailcore import hooks

class WelcomePanel(object):
    order = 50

    def render(self):
        return mark_safe("""
        <section class="panel summary nice-padding">
          <h3>No, but seriously -- welcome to the admin homepage.</h3>
        </section>
        """)

@hooks.register('construct_homepage_panels')
def add_another_welcome_panel(request, panels):
  return panels.append( WelcomePanel() )