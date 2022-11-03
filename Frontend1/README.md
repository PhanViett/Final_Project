#Internationalization (i18n)

1. Update `src/_metronic/partials/layout/header-menus/Languages.tsx`

```
const languages = [
{
    lang: "en",
    name: "English",
    flag: toAbsoluteUrl("/media/flags/united-states.svg")
},
+ {
    +   lang: "tr",
    +   name: "Turkish",
    +   flag: toAbsoluteUrl("/media/flags/turkey.svg")
+ },
{
```

2. Thêm mới `src/_metronic/i18n/messages/tr.json`
3. Tạo vào list ngon ngữ : `src/_metronic/i18n/I18nProvider.tsx`
4. Custom ngôn ngữ : `src/_metronic/i18n/messages/en.json`

```
{"HOME.HELLO": "Hello, {name}!"}

import { FormattedMessage } from "react-intl";

export default function Hello({ name }) {
 return ;
}


import { useIntl } from "react-intl";

export default function Hello({ name }) {
 const intl = useIntl();
 return <h3>{intl.formatMessage({ id: "HOME.HELLO" }, { name })}</h3>
}

```
