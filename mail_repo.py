from properties import HC_URL


def create_reg_mail(name, link):
    body, text = _get_from_template('reg')
    body = body.format(name=name, link=link, HC_URL=HC_URL)
    text = text.format(name=name, link=link, HC_URL=HC_URL)
    return body, text


def create_invite_mail(from_user, invited_user):
    body, text = _get_from_template('invite')
    body = body.format(from_user=from_user, invited_user=invited_user, HC_URL=HC_URL)
    text = text.format(invited_user=invited_user, from_user=from_user, HC_URL=HC_URL)
    return body, text


def _get_from_template(template_name):
    with open('templates/' + template_name + '.html', 'r') as html_file:
        body = html_file.read().replace("\n", "")

    with open('templates/' + template_name + '.txt', 'r') as text_file:
        text = text_file.read()
    return body, text


def _example():
    print(create_invite_mail("user1", "user2"))
    print(create_reg_mail("user", "links234"))


if __name__ == "__main__":
    _example()

