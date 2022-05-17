%global __requires_exclude ^lib%{name}.so|^lib%{name}-js.so

%global gjs_version 1.17.1
%global cinnamon_desktop_version 5.2.0
%global cinnamon_translations_version 5.2.0
%global gobject_introspection_version 1.38.0
%global muffin_version 5.2.0
%global json_glib_version 0.13.2

%global __python %{__python3}

Name:           cinnamon
Version:        5.2.7
Release:        1
Summary:        Window management and application launching for GNOME
License:        GPLv2+ and LGPLv2+
URL:            https://github.com/linuxmint/%{name}
Source0:        https://github.com/linuxmint/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        polkit-%{name}-authentication-agent-1.desktop
Source2:        10_cinnamon-common.gschema.override
Source3:        10_cinnamon-apps.gschema.override.in

Patch0:         autostart.patch
Patch1:         set_wheel.patch
#Patch2:         revert_25aef37.patch
Patch3:         default_panal_launcher.patch
Patch4:         remove_crap_from_menu.patch
Patch5:	        using-gjs.patch

ExcludeArch:    %{ix86}

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  desktop-file-utils
BuildRequires:  python3-rpm-macros
BuildRequires:  pkgconfig(gjs-1.0) >= %{gjs_version}
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gnome-bluetooth-1.0)
BuildRequires:  pkgconfig(libgnome-menu-3.0)
BuildRequires:  pkgconfig(lib%{name}-menu-3.0)
BuildRequires:  pkgconfig(%{name}-desktop) >= %{cinnamon_desktop_version}
BuildRequires:  gobject-introspection >= %{gobject_introspection_version}
BuildRequires:  pkgconfig(json-glib-1.0) >= %{json_glib_version}
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(libnm)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(gudev-1.0)

# for screencast recorder functionality
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  intltool
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libsoup-2.4)

# used in unused BigThemeImage
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libmuffin) >= %{muffin_version}
BuildRequires:  pkgconfig(libpulse)

# Bootstrap requirements
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  gnome-common

# media keys
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(colord)
%ifnarch s390 s390x
BuildRequires:  pkgconfig(libwacom)
BuildRequires:  pkgconfig(xorg-wacom)
%endif
BuildRequires:  pkgconfig(xtst)

Requires:       %{name}-desktop%{?_isa} >= %{cinnamon_desktop_version}
Requires:       muffin%{?_isa} >= %{muffin_version}
Requires:       gjs%{_isa} >= %{gjs_version}
Requires:       gnome-menus%{?_isa} >= 3.0.0-2

# wrapper script used to restart old GNOME session if run --replace
# from the command line
Requires:       gobject-introspection%{?_isa} >= %{gobject_introspection_version}

# needed for loading SVG's via gdk-pixbuf
Requires:       librsvg2%{?_isa}

# needed as it is now split from Clutter
Requires:       json-glib%{?_isa} >= %{json_glib_version}
Requires:       upower%{?_isa}
Requires:       polkit%{?_isa} >= 0.100

# needed for session files
Requires:       %{name}-session%{?_isa}

# needed for schemas
Requires:       at-spi2-atk%{?_isa}

# needed for on-screen keyboard
Requires:       caribou%{?_isa}

# needed for the user menu
Requires:       accountsservice-libs%{?_isa}

# needed for settings
Requires:       libtimezonemap%{?_isa}
Requires:       python3-distro
Requires:       python3-pytz
Requires:       python3-pexpect
Requires:       python3-gobject%{?_isa}
Requires:       python3-dbus%{?_isa}
Requires:       python3-lxml%{?_isa}
Requires:       python3-pillow%{?_isa}
Requires:       python3-pam
Requires:       python3-tinycss2
Requires:       python3-requests
Requires:       python3-setproctitle%{?_isa}
Requires:       python3-xapp
Requires:       mintlocale
Requires:       %{name}-control-center%{?_isa}
Requires:       %{name}-translations >= %{cinnamon_translations_version}

# needed for theme overrides
Requires:       gnome-backgrounds
Requires:       system-logos

# Theming
Requires:       google-noto-sans-fonts
Requires:       %{name}-themes >= 1:1.7.4-0.2.20181112gitb94b890

# RequiredComponents in the session files
Requires:       nemo%{?_isa}
Requires:       %{name}-screensaver%{?_isa}

# metacity and tint2 are needed for fallback
Requires:       metacity%{?_isa}
Requires:       tint2%{?_isa}

# required for keyboard applet
Requires:       xapps%{?_isa}
Requires:       python3-xapps-overrides%{?_isa}

# required for calendar applet
Recommends:     gnome-calendar

# required for network applet
Requires:       nm-connection-editor%{?_isa}
Requires:       network-manager-applet%{?_isa}

Requires:       python3-inotify


# required for cinnamon-killer-daemon
Requires:       keybinder3%{?_isa}

# required for sound applet
Requires:       wget%{?_isa}

# required for printer applet
Requires:       cups-client%{?_isa}

Provides:       desktop-notification-daemon
Provides:       bundled(libcroco) = 0.6.12

%description
Cinnamon is a Linux desktop which provides advanced
innovative features and a traditional user experience.

The desktop layout is similar to Gnome 2.
The underlying technology is forked from Gnome Shell.
The emphasis is put on making users feel at home and providing
them with an easy to use and comfortable desktop experience.

%package devel-doc
Summary: Development Documentation files for Cinnamon
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description devel-doc
This package contains the code documentation for various Cinnamon components.

%prep
%autosetup -p1

%{__sed} -i -e 's@gksu@pkexec@g' files%{_bindir}/%{name}-settings-users
%{__sed} -i -e 's@gnome-orca@orca@g' files%{_datadir}/%{name}/%{name}-settings/modules/cs_accessibility.py
# remove mintlocale im from settings
%{__sed} -i -e 's@mintlocale im@mintlocale_im_removed@g' files%{_datadir}/%{name}/%{name}-settings/%{name}-settings.py

# Fix rpmlint errors
for file in files%{_datadir}/%{name}/%{name}-settings/bin/*.py files%{_datadir}/%{name}/%{name}-looking-glass/*.py \
   files%{_datadir}/%{name}/%{name}-settings/modules/cs_{applets,desklets}.py; do
   chmod a+x $file
done
chmod a-x files%{_datadir}/%{name}/%{name}-settings/bin/__init__.py

%build
%meson \
 --libexecdir=%{_libexecdir}/cinnamon/ \
 -Ddeprecated_warnings=false \
 -Dpy3modules_dir=%{python3_sitelib} \
 -Ddocs=true

%meson_build


%install
%meson_install

# install polkit autostart desktop file
%{__install} --target-directory=%{buildroot}%{_datadir}/applications \
    -Dpm 0644 %{SOURCE1}

# install common gschema override
%{__install} --target-directory=%{buildroot}%{_datadir}/glib-2.0/schemas \
    -Dpm 0644 %{SOURCE2}

# install gschema-override for apps
%{__sed} -e 's!@pkg_manager@!org.mageia.dnfdragora.desktop!g' \
    < %{SOURCE3} > %{buildroot}%{_datadir}/glib-2.0/schemas/10_%{name}-apps.gschema.override

# install gschema-override for wallpaper
%{__cat} >> %{buildroot}%{_datadir}/glib-2.0/schemas/10_%{name}-wallpaper.gschema.override << EOF
[org.cinnamon.desktop.background]
picture-uri='file:///usr/share/backgrounds/tiles/default_blue.jpg'
EOF

# Provide symlink for the background-propeties.
%{__ln_s} %{_datadir}/gnome-background-properties %{buildroot}%{_datadir}/%{name}-background-properties


%check
%{_bindir}/desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files
%doc README.rst AUTHORS
%license COPYING
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/xdg/menus/*
%{_datadir}/applications/*
%{_datadir}/dbus-1/services/org.*.service
%{_datadir}/desktop-directories/*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/%{name}-session/sessions/*
%{_datadir}/icons/hicolor/*/*/*.svg
%{_datadir}/polkit-1/actions/org.%{name}.settings-users.policy
%{_datadir}/xsessions/*
%{_datadir}/%{name}/
%{_datadir}/%{name}-background-properties
%{_libdir}/%{name}/
%{_libexecdir}/%{name}/
%{_mandir}/man1/*
%{python3_sitelib}/cinnamon/

%files devel-doc
%doc %{_datadir}/gtk-doc/html/*/

%changelog
* Sat May 07 2022 Wenlong Ding <wenlong.ding@turbolinux.com.cn> - 5.2.7-1
- Using gjs replace cjs
- Initial package.
