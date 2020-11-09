************************************
 Data System Technology 873 WebSite
************************************

This is a buildout_ for the Data System Technology Office (873) website.


Deploying the Site
==================

It's easy, just extract the tarball containing the software to its final
resting place, say /usr/local/dst-site.  (Of course, you've already done
that, because otherwise how are you reading this README?)

Let's call that final resting place the $INSTALL_DIR.

Next, edit $INSTALL_DIR/operations.cfg and:

* Make sure the ports in the [ports] section are free and that the "zope" port
  matches what's already in Apache's httpd.conf.
* Make sure the user "dstdeploy" is correct and if not fix the [users]
  section.
* Come up with much better passwords in the [passwords] section.  No,
  seriously, *do it*!

Then:

1.  cd $INSTALL_DIR
2.  sudo chmod 600 operations.cfg
3.  sudo /usr/bin/python2.6 bootstrap.py -d -c operations.cfg
4.  sudo bin/buildout -c operations.cfg
5.  Go for a coffee break, step 4 takes a *long* time.
6.  sudo install -o root -g root -m 755 bin/dst-site /etc/init.d
7.  sudo install -o root -g root -m 644 var/etc/logrotate.conf /etc/logrotate.d/dst-site
8.  sudo install -o root -g root -m 755 bin/zope-backup /etc/cron.daily/dst-site
9.  sudo install -o root -g root -m 755 bin/zeopack /etc/cron.monthly/dst-site
10. sudo chkconfig --add dst-site
11. sudo tar xf initialcontent.tar
12. sudo chown -R dstdeploy parts var
13. sudo service dst-site start


Feedback, Bug Reports, Etc.
===========================

Email to sean.kelly@jpl.nasa.gov.


.. References:
.. _buildout: http://www.buildout.org/
