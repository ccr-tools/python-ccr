# Maintainer: george <rpubaddr0 {at} gmail [dot] com>

pkgname=python2-ccr
pkgver=0.2
pkgrel=1
pkgdesc='A python library for accessing and working with the CCR.'
arch=('i686' 'x86_64')
url='http://github.com/ccr-tools/python-ccr/'
license=('GPLv2 or any later version')
depends=('python2')
makedepends=('python-distribute')
source=("")
sha256sums=('a')

package() {
  cd "${pkgname}-${pkgver}"
  python setup.py install --root="${pkgdir}/"
}
