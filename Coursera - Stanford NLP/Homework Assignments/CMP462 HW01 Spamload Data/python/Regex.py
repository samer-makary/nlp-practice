DOT = '(?:\.|\s*\(do?[tm]\)\s*|\s+do?[tm]\s+)'
USER = '(\w+(?:%s\w+)*)' % DOT
AT = '(?:\s*\@\s*|\s*\(at\)\s*|\s+at\s+|\s*&#x40\s*;|\s*&#64;\s*)'
DOMAIN = '((?:\w+(?:[\:\-\,\;]|%s))+[a-z]{2,4})' % DOT
FOLLOWED_BY = '(?:\(?followed by (?:"|&ldquo;)%s%s(?:"|&rdquo;)\)?)' % (AT, DOMAIN)
MP_1 = '%s%s%s' % (USER, AT, DOMAIN)
MP_2 = '%s\s+%s' % (USER, FOLLOWED_BY)
MP_3 = 'e\-?mail\s*[\:\-\,\;]?\s*%s%s((?:\w+\s+)+[a-z]{2,4})' % (USER, AT)
MP_4 = '<address>\s*%s\s+where\s+%s' % (USER, DOMAIN)
MAIL = '(?:%s|%s|%s|%s)' % (MP_1, MP_2, MP_3, MP_4)
print MAIL

ERROR = '<title>40[0-9] [\w\s]+</title>'
print ERROR

# 650-723-0293 OR 650 723-0293
DELIM = '(?:\s*\-\s*|\s+)'
PP_1 = '[0-9]{3}%s[0-9]{3}%s[0-9]{4}' % (DELIM, DELIM)
# (650)723-0293
PP_2 = '\([0-9]{3}\)\s*[0-9]{3}%s[0-9]{4}' % DELIM
PHONE = '(?:%s|%s)' % (PP_1, PP_2)
print PHONE