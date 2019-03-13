import config
import imaplib
import email
from logger import Logger


def read_mail():
    try:
        mail = imaplib.IMAP4_SSL(config.smtp_server)
        mail.login(config.email_login, config.email_pass)
        if mail.select() == 0:
            return None

        result = []

        status, data = mail.search(None, 'ALL')
        id_list = data[0]
        if len(id_list) == 0:
            return result
        id_list = list(map(lambda elem: int(elem), id_list.split()))

        for i in range(max(id_list), min(id_list) - 1, -1):
            status, data = mail.fetch(bytes(str(i), "ascii"), '(RFC822)')
            msg = email.message_from_bytes(data[0][1])

            sender = msg.get('From')
            body = None
            if msg.is_multipart():
                for part in msg.walk():
                    # skip any text/plain (txt) attachments
                    if part.get_content_type() == 'text/plain' and 'attachment' not in str(part.get('Content-Disposition')):
                        body = part.get_payload(decode=True)
                        # break
            # not multipart - i.e. plain text, no attachments, keeping fingers crossed
            else:
                body = msg.get_payload(decode=True)

            result.append({
                'sender': sender,
                'body': body.decode('utf-8')
            })
        return result

    except Exception as e:
        Logger().error_message(e)


if __name__ == '__main__':
    res = read_mail()
    print(res)

