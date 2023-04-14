# encoding: utf-8

'''📀🔬 Data Science: initial content blooming.'''

# from robots.models import Rule, DisallowedUrl

from content.models import HomePage, FlexPage, NewsIndex, NewsItem, CaptchaEmailForm, CaptchaEmailFormField
from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from theme.models import Footer
from wagtail.images.models import Image
from wagtail.models import Site, Page
from wagtail.rich_text import RichText
from wagtailmenus.models import FlatMenu, FlatMenuItem
import pkg_resources, codecs, csv, datetime


class Command(BaseCommand):
    '''Bloom the data science site with initial content and settings.'''

    help = 'Bloom the data science site with initial content and settings'
    search_description = 'Data Science at the Jet Propulsion Laboratory creates insights from large scale scientific data'

    def get_html_text(self, name: str) -> RichText:
        return RichText(pkg_resources.resource_string(__name__, f'data/{name}.html').decode('utf-8').strip())

    def set_site(self):
        '''Set up the Site object for Data Science, returning it.'''
        site = Site.objects.filter(is_default_site=True).first()
        site.site_name = 'Data Science'
        site.hostname = 'datascience.jpl.nasa.gov'
        site.save()
        old_root = site.root_page.specific
        if old_root.title == 'Data Science':
            return site

        with pkg_resources.resource_stream(__name__, 'data/home-banner.jpg') as f:
            banner_image = ImageFile(f, name='data-science-banner-image')
            image = Image(title='Data Science Banner Image', file=banner_image)
            image.save()
            mega_root = old_root.get_parent()
            home_page = HomePage(
                title='Data Science', seo_title='Data Science at the Jet Propulsion Laboratory',
                search_description=self.search_description, banner=image, live=True, slug=old_root.slug,
                depth=old_root.depth, url_path=old_root.url_path, path=old_root.path
            )
            home_page.body.append(('rich_text', self.get_html_text('home')))
            site.root_page = home_page
            old_root.delete()
            mega_root.save()
            home_page.save()
            site.save()
            return site

    def add_initiatives(self, home_page):
        page = FlexPage(title='Initiatives', live=True, show_in_menus=True)
        home_page.add_child(instance=page)
        page.body.append(('rich_text', self.get_html_text('initiatives')))
        page.save()

    def add_technologies(self, home_page):
        page = FlexPage(title='Technologies', live=True, show_in_menus=True)
        home_page.add_child(instance=page)
        page.save()

    def add_workshops(self, home_page):
        page = FlexPage(title='Workshops', live=True, show_in_menus=True)
        home_page.add_child(instance=page)
        page.body.append(('rich_text', self.get_html_text('workshops')))
        page.save()

    def add_news_items(self, news_page):
        io = pkg_resources.resource_stream(__name__, 'data/news.csv')
        utf8_reader = codecs.getreader('utf-8')
        c = csv.reader(utf8_reader(io))
        for title, date, summary, image_fn, image_title, caption, body_fn in c:
            if image_fn:
                with pkg_resources.resource_stream(__name__, f'data/news/{image_fn}') as image_io:
                    image_file = ImageFile(image_io, name=image_fn)
                    image = Image(title=image_title, file=image_file)
                    image.save()
            else:
                image = None
            body = RichText(pkg_resources.resource_string(__name__, f'data/news/{body_fn}').decode('utf-8').strip())
            release_date = datetime.date.fromisoformat(date)
            item = NewsItem(
                title=title, search_description=summary, release_date=release_date, lead_image=image, caption=caption,
                live=True, show_in_menus=False,
            )
            item.body.append(('rich_text', body))
            news_page.add_child(instance=item)
            item.save()

    def add_news(self, home_page):
        page = NewsIndex(title='News', live=True, show_in_menus=True)
        home_page.add_child(instance=page)
        page.save()
        self.add_news_items(page)

    def add_people(self, home_page):
        page = FlexPage(title='People', live=True, show_in_menus=True)
        home_page.add_child(instance=page)
        page.save()

    def add_success(self, home_page):
        page = FlexPage(title='Success Stories', live=True, show_in_menus=True)
        home_page.add_child(instance=page)
        page.save()

    def add_contact(self, home_page):
        page = CaptchaEmailForm(
            title='Contact Us', live=True, show_in_menus=False,
            intro="<p>Want to get in touch? Simply fill out the form below and we'll reach out.</p>",
            outro="<p>Please note that inquiries usually get a response within 3–5 business days.</p>",
            thank_you_text="<p>Thanks! We'll respond back via email in 3–5 business days.</p>",
            from_address='sean.kelly@jpl.nasa.gov',
            to_address='sean.kelly@jpl.nasa.gov',
            subject='Data Science Website: "contact us" form submission',
        )
        home_page.add_child(instance=page)
        page.save()
        page.form_fields.add(CaptchaEmailFormField(
            label='Your Name', field_type='singleline', required=True,
            help_text='Please enter your name.'
        ))
        page.form_fields.add(CaptchaEmailFormField(
            label='Email Address', field_type='email', required=True,
            help_text='Please enter your email address so we can respond back to you.'
        ))
        page.form_fields.add(CaptchaEmailFormField(
            label='Message', field_type='multiline', required=True,
            help_text="What's on your mind?"
        ))
        page.save()

    def add_pages(self, home_page):
        self.add_initiatives(home_page)
        self.add_technologies(home_page)
        self.add_workshops(home_page)
        self.add_news(home_page)
        self.add_people(home_page)
        self.add_success(home_page)
        self.add_contact(home_page)

    def set_initial_settings(self, site):
        footer = Footer.objects.get_or_create(site_id=site.id)[0]
        footer.site_manager = 'Dan Crichton'
        footer.webmaster = 'Sean Kelly'
        footer.clearance = 'CL № 18-0862'
        footer.save()

    def create_footer_menus(self, site):
        FlatMenu.objects.all().delete()

        # For some reason (possibly because contact-us is a form, not a page), the contact us never gets
        # rendered. So I'm rendering it manually in footer.html.
        #
        # Leaving this code in here in case we want to revisit it:
        #
        # contact = FlatMenu(site=site, title='1: Contact', handle='footer-contact', heading='Contact')
        # contact.save()
        # contact_page = Page.objects.filter(slug='contact-us').first()
        # FlatMenuItem(menu=contact, link_page=contact_page, link_text='Contact Us').save()
        # FlatMenuItem(
        #     menu=contact, link_url='https://www.jpl.nasa.gov/who-we-are/media-information/jpl-media-contacts',
        #     link_text='JPL Media Contacts'
        # ).save()

        science = FlatMenu(site=site, title='2: Science', handle='footer-science', heading='Science')
        science.save()
        for slug in ('initiatives', 'technologies', 'workshops'):
            page = Page.objects.filter(slug=slug).first()
            FlatMenuItem(menu=science, link_page=page).save()

        info = FlatMenu(site=site, title='3: Information', handle='footer-info', heading='More Information')
        info.save()
        for slug in ('news', 'people'):
            page = Page.objects.filter(slug=slug).first()
            FlatMenuItem(menu=info, link_page=page).save()

        social = FlatMenu(site=site, title='4: Social Media', handle='footer-social', heading='Social Media')
        social.save()
        for url, text in (
            ('https://www.facebook.com/NASAJPL', 'Facebook'),
            ('https://twitter.com/NASAJPL', 'Twitter'),
            ('https://www.youtube.com/user/JPLnews', 'YouTube'),
            ('https://www.instagram.com/nasajpl/', 'Instagram')
        ):
            FlatMenuItem(menu=social, link_url=url, link_text=text).save()

    def handle(self, *args, **options):
        try:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = False
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = False
            site = self.set_site()
            root = site.root_page
            root.get_children().delete()
            root.refresh_from_db()
            self.add_pages(root)
            self.set_initial_settings(site)
            self.create_footer_menus(site)
        finally:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = True
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = True
