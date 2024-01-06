![Effective Error Handling in Golang](/blog/generated/assets/images/golang-errors/header-800-cbfedf150.jpg)

[Blog](/blog/)
/
[Tutorials](/blog/categories/tutorials/)

- [The Error Type](#the-error-type)
  - [Constructing Errors](#constructing-errors)
  - [Defining Expected Errors](#defining-expected-errors)
    - [Defining Sentinel Errors](#defining-sentinel-errors)
    - [Defining Custom Error Types](#defining-custom-error-types)
- [Wrapping Errors](#wrapping-errors)
  - [The Old Way (Before Go 1.13)](#the-old-way-before-go-1.13)
  - [Errors Are Better Wrapped](#errors-are-better-wrapped)
    - [When To Wrap](#when-to-wrap)
- [Conclusion](#conclusion)
- [References](#references)

You may also enjoy

[![](<>)](/blog/the-roi-of-fast/)

[A biased take on the ROI of fast](/blog/the-roi-of-fast/)

9 minute read

Fast builds with Earthly can lead to significant cost savings in CI/CD infrastructure and increased developer productivity, resulting in a 13X greater value....

[![](<>)](/blog/the-world-deserves-better-builds/)

[The world deserves better builds](/blog/the-world-deserves-better-builds/)

4 minute read

Learn how Earthly is revolutionizing the build process with its self-contained, reproducible, and parallel approach. Say goodbye to slow, brittle builds and ...

[![](<>)](/blog/what-makes-earthly-fast/)

[What makes Earthly fast](/blog/what-makes-earthly-fast/)

13 minute read

Earthly makes CI/CD builds faster by reusing computation from previous runs for unchanged parts of the build. It is particularly effective in speeding up CI ...

[![](<>)](/blog/python-earthly/)

[Better Dependency Management in Python](/blog/python-earthly/)

6 minute read

Learn how Earthly can simplify dependency management in Python projects, ensuring consistency across different environments and streamlining the build and de...

[![](<>)](/blog/introducing-earthly-build-automation-for-the-container-era/)

[Introducing Earthly: build automation for the container era](/blog/introducing-earthly-build-automation-for-the-container-era/)

3 minute read

Introducing Earthly, a build automation tool for the container era. Learn how Earthly brings modern capabilities like reproducibility, determinism, and paral...

[![](<>)](/blog/platform-values/)

[The Platform Values of Earthly](/blog/platform-values/)

10 minute read

Learn about the platform values of Earthly, a new approach to build automation. Discover the principles that guide Earthly’s design, including versatility, a...

[![](<>)](/blog/earthly-github-actions/)

[Better Together - Earthly + Github Actions](/blog/earthly-github-actions/)

15 minute read

Learn how Earthly and Github Actions can work together to improve your Continuous Integration (CI) process. Discover the benefits of Earthly’s local CI pipel...

[![](<>)](/blog/better-builds/)

[Can We Build Better?](/blog/better-builds/)

4 minute read

Learn how to solve the problem of reproducible builds with Earthly, an open-source tool that encapsulates your build process in a Docker-like syntax. With Ea...

![](https://t.co/i/adsct?bci=3&eci=2&event_id=16e0a807-6df5-48fa-b2b5-43369f02d145&events=%5B%5B%22pageview%22%2C%7B%7D%5D%5D&integration=advertiser&p_id=Twitter&p_user_id=0&pl_id=6d6b67af-2220-4959-85f2-0afd69f33e44&tw_document_href=https%3A%2F%2Fearthly.dev%2Fblog%2Fgolang-errors%2F&tw_iframe_status=0&tw_order_quantity=0&tw_sale_amount=0&txn_id=o5s6p&type=javascript&version=2.3.29)![](https://analytics.twitter.com/i/adsct?bci=3&eci=2&event_id=16e0a807-6df5-48fa-b2b5-43369f02d145&events=%5B%5B%22pageview%22%2C%7B%7D%5D%5D&integration=advertiser&p_id=Twitter&p_user_id=0&pl_id=6d6b67af-2220-4959-85f2-0afd69f33e44&tw_document_href=https%3A%2F%2Fearthly.dev%2Fblog%2Fgolang-errors%2F&tw_iframe_status=0&tw_order_quantity=0&tw_sale_amount=0&txn_id=o5s6p&type=javascript&version=2.3.29)
