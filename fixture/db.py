import pymysql.cursors
from model.group import Group
from model.add_new import AddNew
import re


class DbFixture:

    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host=host, database=name, user=user, password=password, autocommit=True)

    def get_group_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select group_id, group_name, group_header, group_footer from group_list")
            for row in cursor:
                (id, name, header, footer) = row
                list.append(Group(id=str(id), name=name, header=header, footer=footer))
        finally:
            cursor.close()
        return list

    def get_contact_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "select id, firstname, lastname, address, home, mobile, work, email, email2, email3, phone2 from addressbook where deprecated='0000-00-00 00:00:00'")
            for row in cursor:
                (id, firstname, lastname, address, home, mobile, work, email, email2, email3, phone2) = row
                current_contact = AddNew(my_id=str(id), my_f_name=firstname, my_l_name=lastname,
                                         my_home_address=address,
                                         my_h_telefon=home, my_mobile=mobile, my_work_telefon=work,
                                         my_secondary_phone=phone2,
                                         my_company_mail=email, my_second_mail=email2, my_third_mail=email3
                                         )
                final_contact = AddNew(my_id=str(id), my_f_name=self.removing_spaces(firstname),
                                       my_l_name=self.removing_spaces(lastname),
                                       my_home_address=self.removing_spaces(address)
                                       )
                final_contact.all_phones_from_home_page = self.merge_phones_like_on_home_page(current_contact)
                final_contact.all_emails_from_home_page = self.merge_emails_like_on_home_page(current_contact)
                list.append(final_contact)

        finally:
            cursor.close()
        return list

    def destroy(self):
        self.connection.close()

    def clear(self, s):
        return re.sub("[() -]", "", s)

    def merge_phones_like_on_home_page(self, contacts):
        return "\n".join(filter(lambda x: x != "",
                                map(lambda x: self.clear(x),
                                    filter(lambda x: x is not None,
                                           [contacts.my_h_telefon, contacts.my_mobile, contacts.my_work_telefon,
                                            contacts.my_secondary_phone]))))

    def merge_emails_like_on_home_page(self, contacts):

        return "\n".join(filter(lambda x: x != "",
                                map(lambda x: self.clear(x),
                                    filter(lambda x: x is not None,
                                           [contacts.my_company_mail, contacts.my_second_mail,
                                            contacts.my_third_mail]))))

    def removing_spaces(self, s):
        return re.sub("  ", " ", s.strip())
