
# Maintainer: Juan Toca <elan17.programacion@gmail.com>
pkgname=terminal-backgrounds-git
pkgver=r43.d467734
pkgrel=1
pkgdesc="Snake-based ZPG game"
arch=('any')
url="https://github.com/elan17/Terminal-backgrounds"
license=('GPL3')
groups=()
depends=()
makedepends=('git' 'python')
provides=("${pkgname%-VCS}")
conflicts=("${pkgname%-VCS}")
replaces=()
backup=()
options=(!emptydirs)
install=
source=('snakes-git::git+https://github.com/elan17/Terminal-backgrounds#branch=master')
noextract=()
md5sums=('SKIP')

pkgver() {
  cd "$pkgname"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
	cd "$srcdir/$pkgname"
  	install -Dm 755 ./snakes/snakes.py "${pkgdir}/usr/bin/snakes"
  	install -Dm 644 ./snakes/LICENSE "${pkgdir}/usr/share/doc/${pkgname}/LICENSE"
}
