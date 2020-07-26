pkgname=qtile-widget-unitstatus-git
_pkgname=qtile-widget-unitstatus
pkgver=r2.5c5f46b
pkgrel=1
provides=("$_pkgname")
conflicts=("$_pkgname")
pkgdesc="Qtile widget to display status of systemd unit."
url="https://github.com/elparaguayo/qtile-widget-unitstatus.git"
arch=("any")
license=("MIT")
depends=("python" "qtile" "python-pydbus")
source=("git+https://github.com/elparaguayo/$_pkgname.git")
md5sums=("SKIP")

pkgver()
{
  cd "$_pkgname"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package()
{
  cd "$_pkgname"
  python setup.py install --root="$pkgdir"
}
