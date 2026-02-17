# Changelog

## [0.5.0-beta.2](https://github.com/chriskauffman/test-db/compare/v0.5.0-beta.1...v0.5.0-beta.2) (2026-02-17)


### Features

* **_job:** job position added and attributes removed ([8e041e5](https://github.com/chriskauffman/test-db/commit/8e041e5eba94b1af2a91eb32006b709fca710307))


### Miscellaneous Chores

* release 0.5.0-beta.2 ([8667938](https://github.com/chriskauffman/test-db/commit/8667938997c6e94cb3861f8f01abaceb349136c0))

## [0.5.0-beta.1](https://github.com/chriskauffman/test-db/compare/v0.5.0-beta.1...v0.5.0-beta.1) (2026-02-15)


### release

* beta.1 ([59f3132](https://github.com/chriskauffman/test-db/commit/59f31321014bbce22fb5c7b196b2dffbb8577ecd))
* relase new alpha version ([cfb5c04](https://github.com/chriskauffman/test-db/commit/cfb5c043e07f480a07e802f59794a19db49916c0))


### Features

* **cmd2:** add command updated to use latest automatic data generation ([b7db6ae](https://github.com/chriskauffman/test-db/commit/b7db6ae789060d6e2e110dd8ee19ba42fe5a488c))
* first test-db version forked from rest-api-test ([#1](https://github.com/chriskauffman/test-db/issues/1)) ([15d4ebc](https://github.com/chriskauffman/test-db/commit/15d4ebc1771ab436453bf1cf317817ea17d8e795))
* improved handling in create listeners to avoid duplicate data ([18dad7e](https://github.com/chriskauffman/test-db/commit/18dad7ebdaf2eb692168346c0942c4a0b9ae62e9))
* **tdb:** improved CLI options, shortcut names, such as "-d", now supported ([c505263](https://github.com/chriskauffman/test-db/commit/c505263bf6bd47e5e112e5d6b59527a7f30b9b0f))
* **typer:** bulk add command added ([f9c87e2](https://github.com/chriskauffman/test-db/commit/f9c87e2e3d5abd5f58c4f40b6d812b26f862af3a))
* **typer:** bulk add command added; add command updated to use latest automatic data generation ([82e4a3a](https://github.com/chriskauffman/test-db/commit/82e4a3af25587bef06c7ec4d1c160c42681d7050))


### Bug Fixes

* **cmd2:** corrected misnamed commands ([#67](https://github.com/chriskauffman/test-db/issues/67)) ([ad0ba9b](https://github.com/chriskauffman/test-db/commit/ad0ba9ba1913d66f8f1b2b9218b54494e31c7ddf)), closes [#66](https://github.com/chriskauffman/test-db/issues/66)
* **cmd2:** missing return on error condition ([0040af2](https://github.com/chriskauffman/test-db/commit/0040af2034b6235c3e1bd70f46e366a69d3f7eed))
* **cmd2:** remove `add_help=False` from cmd2 commands ([#70](https://github.com/chriskauffman/test-db/issues/70)) ([d5e1fa1](https://github.com/chriskauffman/test-db/commit/d5e1fa1f4ceb90f6eb2ca51069eac8b224262e04)), closes [#69](https://github.com/chriskauffman/test-db/issues/69)
* correct list command in utilities for entity key values ([#39](https://github.com/chriskauffman/test-db/issues/39)) ([82b45bc](https://github.com/chriskauffman/test-db/commit/82b45bcebf6a23f8d0b2d2611845a5cc4085f5e0)), closes [#38](https://github.com/chriskauffman/test-db/issues/38)
* improve acceptNull handling on input; allow key value to accept null/none ([5046a54](https://github.com/chriskauffman/test-db/commit/5046a54862647d0910393aeeab8899efd4250b74))
* invalid escape sequence ([#33](https://github.com/chriskauffman/test-db/issues/33)) ([ad1a5b4](https://github.com/chriskauffman/test-db/commit/ad1a5b48405b7e4878d3ecb4ba4acf6b141ea1de)), closes [#30](https://github.com/chriskauffman/test-db/issues/30)
* make sure visual ID and view methods display gID first and use correct elements ([2d4523d](https://github.com/chriskauffman/test-db/commit/2d4523dbca4b844af5b9090bbfc7e73f13809532))
* organization view missing details ([#23](https://github.com/chriskauffman/test-db/issues/23)) ([a657bab](https://github.com/chriskauffman/test-db/commit/a657bab093208ed9e357d143d8b80de94754ed16)), closes [#22](https://github.com/chriskauffman/test-db/issues/22)
* **Person:** update typing to indicate that  getPersonalKeyValueSecureByKey always returns a PersonalKeyValueSecure object ([#27](https://github.com/chriskauffman/test-db/issues/27)) ([bc5600a](https://github.com/chriskauffman/test-db/commit/bc5600a91b2a265f4507c03056f77295b20c430b))
* setup release please for prerelease ([d600f1d](https://github.com/chriskauffman/test-db/commit/d600f1df6ed18c4b11d3da0328085770237ac67a))


### Miscellaneous Chores

* release 0.2.0 ([6b8b038](https://github.com/chriskauffman/test-db/commit/6b8b038fb8ea85250f5035bfc6c3d4e9e9084725))
* release 0.3.0 ([0de0515](https://github.com/chriskauffman/test-db/commit/0de0515e45b5c33304db4336289aa22809d9a40c))
* release 0.3.1 ([9bc666c](https://github.com/chriskauffman/test-db/commit/9bc666caae8809c941400273442894586d92e324))
* release 0.3.3 ([783154d](https://github.com/chriskauffman/test-db/commit/783154dfea6bbaa82162cd39929214541b8644b5))
* release 0.4.0 ([b27e388](https://github.com/chriskauffman/test-db/commit/b27e388e9750ef76fa2a9ceb86ab2141462ce43b))
* release 0.4.1 ([0791282](https://github.com/chriskauffman/test-db/commit/079128256ec0e09df26cb3c050584ad1d96532d6))
* release 0.5.0-beta.1 ([87b56e1](https://github.com/chriskauffman/test-db/commit/87b56e131a13d9c3e4b8b13cc2e155bcb8d5e785))
* **release:** relase new alpha version ([2a82a23](https://github.com/chriskauffman/test-db/commit/2a82a23ddb1aa736d8dc0ad7cfccab8e05064444))

## [0.4.1](https://github.com/chriskauffman/test-db/compare/v0.4.0...v0.4.1) (2026-02-07)


### Bug Fixes

* improve acceptNull handling on input; allow key value to accept null/none ([5046a54](https://github.com/chriskauffman/test-db/commit/5046a54862647d0910393aeeab8899efd4250b74))
* make sure visual ID and view methods display gID first and use correct elements ([2d4523d](https://github.com/chriskauffman/test-db/commit/2d4523dbca4b844af5b9090bbfc7e73f13809532))


### Miscellaneous Chores

* release 0.4.1 ([0791282](https://github.com/chriskauffman/test-db/commit/079128256ec0e09df26cb3c050584ad1d96532d6))

## [0.4.0](https://github.com/chriskauffman/test-db/compare/v0.3.3...v0.4.0) (2026-02-02)


### Miscellaneous Chores

* release 0.4.0 ([b27e388](https://github.com/chriskauffman/test-db/commit/b27e388e9750ef76fa2a9ceb86ab2141462ce43b))

## [0.3.3](https://github.com/chriskauffman/test-db/compare/v0.3.2...v0.3.3) (2026-01-11)


### Miscellaneous Chores

* release 0.3.3 ([783154d](https://github.com/chriskauffman/test-db/commit/783154dfea6bbaa82162cd39929214541b8644b5))

## [0.3.2](https://github.com/chriskauffman/test-db/compare/v0.3.1...v0.3.2) (2026-01-07)


### Bug Fixes

* **cmd2:** remove `add_help=False` from cmd2 commands ([#70](https://github.com/chriskauffman/test-db/issues/70)) ([d5e1fa1](https://github.com/chriskauffman/test-db/commit/d5e1fa1f4ceb90f6eb2ca51069eac8b224262e04)), closes [#69](https://github.com/chriskauffman/test-db/issues/69)

## [0.3.1](https://github.com/chriskauffman/test-db/compare/v0.3.0...v0.3.1) (2026-01-07)


### Bug Fixes

* **cmd2:** corrected misnamed commands ([#67](https://github.com/chriskauffman/test-db/issues/67)) ([ad0ba9b](https://github.com/chriskauffman/test-db/commit/ad0ba9ba1913d66f8f1b2b9218b54494e31c7ddf)), closes [#66](https://github.com/chriskauffman/test-db/issues/66)


### Miscellaneous Chores

* release 0.3.1 ([9bc666c](https://github.com/chriskauffman/test-db/commit/9bc666caae8809c941400273442894586d92e324))

## [0.3.0](https://github.com/chriskauffman/test-db/compare/v0.2.0...v0.3.0) (2026-01-07)


### Miscellaneous Chores

* release 0.3.0 ([0de0515](https://github.com/chriskauffman/test-db/commit/0de0515e45b5c33304db4336289aa22809d9a40c))

## [0.3.0-beta.1](https://github.com/chriskauffman/test-db/compare/v0.4.0-beta.0...v0.3.0-beta.1) (2026-01-07)


### Miscellaneous Chores

* release 0.3.0-beta.1 ([f0cb16a](https://github.com/chriskauffman/test-db/commit/f0cb16a382ea07dc04985476f34db8a9c6fa053d))

## [0.4.0-beta.0](https://github.com/chriskauffman/test-db/compare/v0.3.0-beta.0...v0.4.0-beta.0) (2026-01-07)


### Features

* add editing of gID ([#61](https://github.com/chriskauffman/test-db/issues/61)) ([c70217b](https://github.com/chriskauffman/test-db/commit/c70217b7d338aef15c3631bb125072469373af72)), closes [#60](https://github.com/chriskauffman/test-db/issues/60)

## [0.3.0-beta.0](https://github.com/chriskauffman/test-db/compare/v0.3.0-beta.0...v0.3.0-beta.0) (2026-01-06)


### release

* beta.1 ([59f3132](https://github.com/chriskauffman/test-db/commit/59f31321014bbce22fb5c7b196b2dffbb8577ecd))
* relase new alpha version ([cfb5c04](https://github.com/chriskauffman/test-db/commit/cfb5c043e07f480a07e802f59794a19db49916c0))


### Features

* first test-db version forked from rest-api-test ([#1](https://github.com/chriskauffman/test-db/issues/1)) ([15d4ebc](https://github.com/chriskauffman/test-db/commit/15d4ebc1771ab436453bf1cf317817ea17d8e795))


### Bug Fixes

* **cmd2:** missing return on error condition ([0040af2](https://github.com/chriskauffman/test-db/commit/0040af2034b6235c3e1bd70f46e366a69d3f7eed))
* correct list command in utilities for entity key values ([#39](https://github.com/chriskauffman/test-db/issues/39)) ([82b45bc](https://github.com/chriskauffman/test-db/commit/82b45bcebf6a23f8d0b2d2611845a5cc4085f5e0)), closes [#38](https://github.com/chriskauffman/test-db/issues/38)
* invalid escape sequence ([#33](https://github.com/chriskauffman/test-db/issues/33)) ([ad1a5b4](https://github.com/chriskauffman/test-db/commit/ad1a5b48405b7e4878d3ecb4ba4acf6b141ea1de)), closes [#30](https://github.com/chriskauffman/test-db/issues/30)
* organization view missing details ([#23](https://github.com/chriskauffman/test-db/issues/23)) ([a657bab](https://github.com/chriskauffman/test-db/commit/a657bab093208ed9e357d143d8b80de94754ed16)), closes [#22](https://github.com/chriskauffman/test-db/issues/22)
* **Person:** update typing to indicate that  getPersonalKeyValueSecureByKey always returns a PersonalKeyValueSecure object ([#27](https://github.com/chriskauffman/test-db/issues/27)) ([bc5600a](https://github.com/chriskauffman/test-db/commit/bc5600a91b2a265f4507c03056f77295b20c430b))
* setup release please for prerelease ([d600f1d](https://github.com/chriskauffman/test-db/commit/d600f1df6ed18c4b11d3da0328085770237ac67a))


### Miscellaneous Chores

* release 0.2.0 ([6b8b038](https://github.com/chriskauffman/test-db/commit/6b8b038fb8ea85250f5035bfc6c3d4e9e9084725))
* release 0.3.0-beta.0 ([1776f0f](https://github.com/chriskauffman/test-db/commit/1776f0fa76d5fa5e00eb452881dee7691d68cec8))
* **release:** relase new alpha version ([2a82a23](https://github.com/chriskauffman/test-db/commit/2a82a23ddb1aa736d8dc0ad7cfccab8e05064444))

## [0.2.0](https://github.com/chriskauffman/test-db/compare/v0.1.6-beta.1...v0.2.0) (2026-01-01)


### Miscellaneous Chores

* release 0.2.0 ([6b8b038](https://github.com/chriskauffman/test-db/commit/6b8b038fb8ea85250f5035bfc6c3d4e9e9084725))

## [0.2.0-beta.4](https://github.com/chriskauffman/test-db/compare/v0.2.0-beta.3...v0.2.0-beta.4) (2025-12-31)


### Bug Fixes

* needed to catch errors if DB encryption key not set and secure key value accessed ([d8375a9](https://github.com/chriskauffman/test-db/commit/d8375a9977c2445da0e1a2898e3c8d64b6bfe7fe)), closes [#55](https://github.com/chriskauffman/test-db/issues/55)


### Miscellaneous Chores

* release 0.2.0-beta.4 ([c59f3f9](https://github.com/chriskauffman/test-db/commit/c59f3f91be2f1b481335d2b74ff06af64717db18))

## [0.2.0-beta.3](https://github.com/chriskauffman/test-db/compare/v0.2.0-beta.2...v0.2.0-beta.3) (2025-12-30)


### Miscellaneous Chores

* release 0.2.0-beta.3 ([76dbd48](https://github.com/chriskauffman/test-db/commit/76dbd488f360bb8bbc48120ac6452a9785e1bdb1))

## [0.2.0-beta.2](https://github.com/chriskauffman/test-db/compare/v0.2.0-beta.1...v0.2.0-beta.2) (2025-12-29)


### Bug Fixes

* moving logger out of class ([b0183e5](https://github.com/chriskauffman/test-db/commit/b0183e5ae8d079e218171dca65d34cac525909ad)), closes [#51](https://github.com/chriskauffman/test-db/issues/51)
* renamed cmd2 history file ([0edc5dd](https://github.com/chriskauffman/test-db/commit/0edc5dd23d4700187aca48ba2c567eea3a0f2860)), closes [#49](https://github.com/chriskauffman/test-db/issues/49)


### Miscellaneous Chores

* release 0.2.0-beta.2 ([a83099d](https://github.com/chriskauffman/test-db/commit/a83099d076a0247d8e60a1c15e66ff92f3af4703))

## [0.2.0-beta.1](https://github.com/chriskauffman/test-db/compare/v0.2.0-beta.0...v0.2.0-beta.1) (2025-12-29)


### Miscellaneous Chores

* release 0.2.0-beta.1 ([59bafd5](https://github.com/chriskauffman/test-db/commit/59bafd5a0cee382152aa63a31b3a2cae2343d234))

## [0.2.0-beta.0](https://github.com/chriskauffman/test-db/compare/v0.0.0-beta.0...v0.2.0-beta.0) (2025-12-23)


### release

* beta.1 ([59f3132](https://github.com/chriskauffman/test-db/commit/59f31321014bbce22fb5c7b196b2dffbb8577ecd))
* relase new alpha version ([cfb5c04](https://github.com/chriskauffman/test-db/commit/cfb5c043e07f480a07e802f59794a19db49916c0))


### Features

* first test-db version forked from rest-api-test ([#1](https://github.com/chriskauffman/test-db/issues/1)) ([15d4ebc](https://github.com/chriskauffman/test-db/commit/15d4ebc1771ab436453bf1cf317817ea17d8e795))


### Bug Fixes

* **cmd2:** missing return on error condition ([0040af2](https://github.com/chriskauffman/test-db/commit/0040af2034b6235c3e1bd70f46e366a69d3f7eed))
* correct list command in utilities for entity key values ([#39](https://github.com/chriskauffman/test-db/issues/39)) ([82b45bc](https://github.com/chriskauffman/test-db/commit/82b45bcebf6a23f8d0b2d2611845a5cc4085f5e0)), closes [#38](https://github.com/chriskauffman/test-db/issues/38)
* invalid escape sequence ([#33](https://github.com/chriskauffman/test-db/issues/33)) ([ad1a5b4](https://github.com/chriskauffman/test-db/commit/ad1a5b48405b7e4878d3ecb4ba4acf6b141ea1de)), closes [#30](https://github.com/chriskauffman/test-db/issues/30)
* organization view missing details ([#23](https://github.com/chriskauffman/test-db/issues/23)) ([a657bab](https://github.com/chriskauffman/test-db/commit/a657bab093208ed9e357d143d8b80de94754ed16)), closes [#22](https://github.com/chriskauffman/test-db/issues/22)
* **Person:** update typing to indicate that  getPersonalKeyValueSecureByKey always returns a PersonalKeyValueSecure object ([#27](https://github.com/chriskauffman/test-db/issues/27)) ([bc5600a](https://github.com/chriskauffman/test-db/commit/bc5600a91b2a265f4507c03056f77295b20c430b))
* setup release please for prerelease ([d600f1d](https://github.com/chriskauffman/test-db/commit/d600f1df6ed18c4b11d3da0328085770237ac67a))


### Miscellaneous Chores

* release 0.2.0-beta.0 ([6405bc0](https://github.com/chriskauffman/test-db/commit/6405bc0865533c22ab6dce0e526eea8cec6eae3e))
* **release:** relase new alpha version ([2a82a23](https://github.com/chriskauffman/test-db/commit/2a82a23ddb1aa736d8dc0ad7cfccab8e05064444))

## [0.1.6-beta.1](https://github.com/chriskauffman/test-db/compare/v0.1.5-beta.1...v0.1.6-beta.1) (2025-12-23)


### Bug Fixes

* setup release please for prerelease ([d600f1d](https://github.com/chriskauffman/test-db/commit/d600f1df6ed18c4b11d3da0328085770237ac67a))

## [0.1.5-beta.1](https://github.com/chriskauffman/test-db/compare/v0.1.4-beta.1...v0.1.5-beta.1) (2025-12-22)


### Bug Fixes

* correct list command in utilities for entity key values ([#39](https://github.com/chriskauffman/test-db/issues/39)) ([82b45bc](https://github.com/chriskauffman/test-db/commit/82b45bcebf6a23f8d0b2d2611845a5cc4085f5e0)), closes [#38](https://github.com/chriskauffman/test-db/issues/38)

## [0.1.4-beta.1](https://github.com/chriskauffman/test-db/compare/v0.1.3-beta.1...v0.1.4-beta.1) (2025-12-18)


### Bug Fixes

* **cmd2:** missing return on error condition ([0040af2](https://github.com/chriskauffman/test-db/commit/0040af2034b6235c3e1bd70f46e366a69d3f7eed))

## [0.1.3-beta.1](https://github.com/chriskauffman/test-db/compare/v0.1.2-beta.1...v0.1.3-beta.1) (2025-12-18)


### Bug Fixes

* invalid escape sequence ([#33](https://github.com/chriskauffman/test-db/issues/33)) ([ad1a5b4](https://github.com/chriskauffman/test-db/commit/ad1a5b48405b7e4878d3ecb4ba4acf6b141ea1de)), closes [#30](https://github.com/chriskauffman/test-db/issues/30)

## [0.1.2-beta.1](https://github.com/chriskauffman/test-db/compare/v0.1.1-beta.1...v0.1.2-beta.1) (2025-12-12)


### Bug Fixes

* **Person:** update typing to indicate that  getPersonalKeyValueSecureByKey always returns a PersonalKeyValueSecure object ([#27](https://github.com/chriskauffman/test-db/issues/27)) ([bc5600a](https://github.com/chriskauffman/test-db/commit/bc5600a91b2a265f4507c03056f77295b20c430b))

## [0.1.1-beta.1](https://github.com/chriskauffman/test-db/compare/v0.1.1-alpha.3...v0.1.1-beta.1) (2025-12-11)


### release

* beta.1 ([59f3132](https://github.com/chriskauffman/test-db/commit/59f31321014bbce22fb5c7b196b2dffbb8577ecd))

## [0.1.1-alpha.3](https://github.com/chriskauffman/test-db/compare/v0.1.0-alpha.3...v0.1.1-alpha.3) (2025-12-02)


### Bug Fixes

* organization view missing details ([#23](https://github.com/chriskauffman/test-db/issues/23)) ([a657bab](https://github.com/chriskauffman/test-db/commit/a657bab093208ed9e357d143d8b80de94754ed16)), closes [#22](https://github.com/chriskauffman/test-db/issues/22)

## [0.1.0-alpha.3](https://github.com/chriskauffman/test-db/compare/v0.1.0-alpha.3...v0.1.0-alpha.3) (2025-12-02)


### release

* relase new alpha version ([cfb5c04](https://github.com/chriskauffman/test-db/commit/cfb5c043e07f480a07e802f59794a19db49916c0))


### Features

* first test-db version forked from rest-api-test ([#1](https://github.com/chriskauffman/test-db/issues/1)) ([15d4ebc](https://github.com/chriskauffman/test-db/commit/15d4ebc1771ab436453bf1cf317817ea17d8e795))


### Miscellaneous Chores

* **release:** relase new alpha version ([2a82a23](https://github.com/chriskauffman/test-db/commit/2a82a23ddb1aa736d8dc0ad7cfccab8e05064444))

## [0.1.0-alpha.2](https://github.com/chriskauffman/test-db/compare/v0.1.0-alpha.1...v0.1.0-alpha.2) (2025-11-26)


### Miscellaneous Chores

* **release:** relase new alpha version ([2a82a23](https://github.com/chriskauffman/test-db/commit/2a82a23ddb1aa736d8dc0ad7cfccab8e05064444))

## [0.1.0-alpha.1](https://github.com/chriskauffman/test-db/compare/v0.1.0...v0.1.0-alpha.1) (2025-11-22)


### Features

* first test-db version forked from rest-api-test ([#1](https://github.com/chriskauffman/test-db/issues/1)) ([15d4ebc](https://github.com/chriskauffman/test-db/commit/15d4ebc1771ab436453bf1cf317817ea17d8e795))
