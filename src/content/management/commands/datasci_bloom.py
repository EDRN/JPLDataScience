# encoding: utf-8

'''📀🔬 Data Science: initial content blooming.'''

# from robots.models import Rule, DisallowedUrl

from content.models import HomePage, FlexPage
from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from theme.models import Footer
from wagtail.images.models import Image
from wagtail.models import Site, Page
from wagtail.rich_text import RichText
from wagtailmenus.models import FlatMenu, FlatMenuItem
import pkg_resources


class Command(BaseCommand):
    '''Bloom the data science site with initial content and settings.'''

    help = 'Bloom the data science site with initial content and settings'
    search_description = 'Data Science at the Jet Propulsion Laboratory creates insights from large scale scientific data'
    home_page_text = '''<p>Bits how suspended heavy hypatia hidden preserve mote helmets. Love galaxyrise impossible bearable seed starlight gravity require ghostly bearable vastness tesseract vanquish. Syntheses small away made global starlight brain dream mote. Flourish hearts cluster venture eye gravity bits syntheses star stuff suspended s with two billions by. Mind dream root glorious home ever atoms gravity global.</p>

<p>Two universe that global astonishment root still explosion dust ash. Rogue astonishment glorious figures tingling prime small gathered hearts. Figures energy matter explosion with something incredible invent edge something incredible cluster away universe. Figures universe beings interiors still that mote astonishment calls to us bearable sunrise still finite but unbounded arena cambrian. That hearts rogue by spine number still stirred ve universe stellar alchemy kindling astonishment preserve.</p>

<p>Star stuff root not galaxies courage ever small explosion rich helmets science from which we spring. Starlight extraordinary made number starlight tingling explosion death pale blue dot dawn paroxysm are starlight. Intelligent star stuff kindling pretty glorious heavy billions collapsing stars. Cherish harvesting not mote questions ocean waiting be known coveralls energy sunrise kindling pale blue dot. Forever eye glorious love waiting be known syntheses globular more claims.</p>

<p>Stellar alchemy by away how cluster spine root globular arena brain calls to us ash atoms helmets vanquish. Fluff tingling are ash fugue invent kindling there little by cosmic atoms waiting be known rogue cosmic. Forever stirred finite but unbounded small gathered tingling beings hundreds interiors brilliant. Claims kindling finite but unbounded root ocean bits eye good upon hearts dawn only paroxysm billions. Cherish galaxies tesseract extraordinary arena edge pretty more upon vast number motes.</p>'''

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
            home_page.body.append(('rich_text', RichText(self.home_page_text)))
            site.root_page = home_page
            old_root.delete()
            mega_root.save()
            home_page.save()
            site.save()
            return site

    def add_initiatives(self, home_page):
        page = FlexPage(title='Initiatives', live=True, show_in_menus=True)
        home_page.add_child(instance=page)
        page.save()

    def add_technologies(self, home_page):
        page = FlexPage(title='Technologies', live=True, show_in_menus=True)
        home_page.add_child(instance=page)
        page.save()

    def add_workshops(self, home_page):
        page = FlexPage(title='Workshops', live=True, show_in_menus=True)
        home_page.add_child(instance=page)
        page.save()

    def add_news(self, home_page):
        page = FlexPage(title='News', live=True, show_in_menus=True)
        home_page.add_child(instance=page)
        page.save()

    def add_people(self, home_page):
        page = FlexPage(title='People', live=True, show_in_menus=True)
        home_page.add_child(instance=page)
        page.save()

    def add_contact(self, home_page):
        page = FlexPage(title='Contact Us', live=True, show_in_menus=True)
        home_page.add_child(instance=page)
        page.save()

    def add_pages(self, home_page):
        self.add_initiatives(home_page)
        self.add_technologies(home_page)
        self.add_workshops(home_page)
        self.add_news(home_page)
        self.add_people(home_page)
        self.add_contact(home_page)

    def set_initial_settings(self, site):
        footer = Footer.objects.get_or_create(site_id=site.id)[0]
        footer.site_manager = 'Dan Crichton'
        footer.webmaster = 'Sean Kelly'
        footer.clearance = 'CL № 18-0862'
        footer.save()

    def create_footer_menus(self, site):
        FlatMenu.objects.all().delete()

        contact = FlatMenu(site=site, title='1: Contact', handle='footer-contact', heading='Contact')
        contact.save()
        contact_page = Page.objects.filter(slug='contact-us').first()
        FlatMenuItem(menu=contact, link_page=contact_page).save()
        FlatMenuItem(
            menu=contact, link_url='https://www.jpl.nasa.gov/who-we-are/media-information/jpl-media-contacts',
            link_text='JPL Media Contacts'
        ).save()

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
