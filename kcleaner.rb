class kcleaner < Formula
  include Language::Python::Virtualenv

  desc " A little CLI tool to help keeping Config Files clean"
  homepage "https://fancywhale.ca/"
  url "https://files.pythonhosted.org/packages/ff/d2/c8ef2dc18777b1a01b58513db9a11a9d32173e99b66d4e096358a825bb9a/PyYAML-5.1b1.tar.gz#sha256=b21fadf0e343c3738cc956be9d24ee7a83d3260ff1a6805f860b4f5d4645b7b9"
  sha256 "b21fadf0e343c3738cc956be9d24ee7a83d3260ff1a6805f860b4f5d4645b7b9"
  head "https://github.com/gcarrarom/kubeconfig-cleaner-cli.git"

  # TODO: If you're submitting an existing package, make sure you include your
  #       bottle block here.

  depends_on :python3

  resource "Click" do
    url "https://files.pythonhosted.org/packages/fa/37/45185cb5abbc30d7257104c434fe0b07e5a195a6847506c074527aa599ec/Click-7.0-py2.py3-none-any.whl#sha256=2335065e6395b9e67ca716de5f7526736bfa6ceead690adf616d925bdc622b13"
    sha256 "2335065e6395b9e67ca716de5f7526736bfa6ceead690adf616d925bdc622b13"
  end

  resource "setuptools" do
    url "https://files.pythonhosted.org/packages/d1/6a/4b2fcefd2ea0868810e92d519dacac1ddc64a2e53ba9e3422c3b62b378a6/setuptools-40.8.0-py2.py3-none-any.whl#sha256=e8496c0079f3ac30052ffe69b679bd876c5265686127a3159cfa415669b7f9ab"
    sha256 "e8496c0079f3ac30052ffe69b679bd876c5265686127a3159cfa415669b7f9ab"
  end

  resource "iterfzf" do
    url "https://files.pythonhosted.org/packages/a1/7d/a4a5de90f3cdd825cf9bfcb6ea6270533ec8127b1e328eecf7b499084c59/iterfzf-0.4.0.17.3.tar.gz#sha256=d58497135ea417777e9f518356ca3613198ffa155667a7ac918495cab9c22abb"
    sha256 "d58497135ea417777e9f518356ca3613198ffa155667a7ac918495cab9c22abb"
  end

  def install
    virtualenv_install_with_resources
  end

  # TODO: Add your package's tests here
end