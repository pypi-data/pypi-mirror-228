from datetime import datetime
from enum import IntEnum
from typing import Type
from tortoise import fields
from tortoise.signals import post_save
from tortoise_api_model import Model
from tortoise_api_model.fields import DatetimeSecField


class UserStatus(IntEnum):
    kicked = 0
    member = 1
    administrator = 2

class ClientStatus(IntEnum):
    ended = 0
    waiting = 1
    paused = 2
    active = 3

class AgentStatus(IntEnum):
    banned = 0
    stopped = 1
    runned = 2


class Proxy(Model):
    host: int = fields.CharField(15)
    port: int = fields.IntField()
    login: str = fields.CharField(63)
    password: str = fields.CharField(63)

    agents: fields.BackwardFKRelation["Agent"]

    _icon = 'network'

    def repr(self):
        return f'{self.host}:{self.port}'

    class Meta:
        table_description = "SOCKS5 Proxies"
        unique_together = (("login", "host", "port"),)


class User(Model):
    id: int = fields.BigIntField(pk=True)
    active: int = fields.BooleanField(default=1)
    username: str = fields.CharField(63, null=True, unique=True)
    name: str = fields.CharField(63)
    bio: str = fields.CharField(255, null=True)
    created_at: datetime = DatetimeSecField(auto_now_add=True)
    updated_at: datetime = DatetimeSecField(auto_now=True)
    phone: int = fields.BigIntField(null=True)

    client: fields.BackwardOneToOneRelation["Client"]
    agent: fields.BackwardOneToOneRelation["Agent"]
    chats: fields.ManyToManyRelation["Chat"] = fields.ManyToManyField("models.Chat", 'userinchat')

    _icon = 'user'

    class Meta:
        table_description = "Telegram users"


class Agent(Model):
    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User", related_name="agent")
    user_id: int
    status: AgentStatus = fields.IntEnumField(AgentStatus, default=AgentStatus.stopped)
    sess: str = fields.CharField(511, null=True)
    proxy: fields.ForeignKeyRelation[Proxy] = fields.ForeignKeyField("models.Proxy", related_name="agents")
    proxy_id: int
    created_at: datetime = DatetimeSecField(auto_now_add=True)
    updated_at: datetime = DatetimeSecField(auto_now=True)

    businesses: fields.BackwardFKRelation["Business"]

    _icon = 'spy'

    class Meta:
        table_description = "Agents"


class Client(Model):
    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User", related_name="client")
    user_id: int
    business: fields.ForeignKeyRelation["Business"] = fields.OneToOneField("models.Business", related_name="client", null=True)
    business_id: int
    status: ClientStatus = fields.IntEnumField(ClientStatus, default=ClientStatus.waiting)

    _icon = 'heart-handshake'

    class Meta:
        table_description = "Clients"


class Chat(Model):
    id: int = fields.BigIntField(pk=True)
    is_private: int = fields.BooleanField(default=0)
    is_channel: int = fields.BooleanField(default=0)
    username: str = fields.CharField(63, null=True, unique=True)
    name: str = fields.CharField(63)
    description: str = fields.CharField(255)
    link: str = fields.CharField(127)
    created_at: datetime = DatetimeSecField(auto_now_add=True)
    updated_at: datetime = DatetimeSecField(auto_now=True)

    users: fields.ManyToManyRelation[User] # = fields.ManyToManyField("models.User", 'userinchat')
    businesses: fields.ManyToManyRelation["Business"] # = fields.ManyToManyField("models.Chat", 'chatinbusiness')

    _icon = 'messages'

    class Meta:
        table_description = "Chats/Channels"


class UserInChat(Model):
    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User")
    chat: fields.OneToOneRelation[Chat] = fields.OneToOneField("models.Chat")
    role: UserStatus = fields.IntEnumField(UserStatus, default=UserStatus.member)
    created_at: datetime = DatetimeSecField(auto_now_add=True)

    _icon = 'chat'
    _hidden = True

    class Meta:
        table_description = "User in Chats"


class Region(Model):
    name: str = fields.CharField(127, unique=True)
    parent: fields.ForeignKeyRelation["Region"] = fields.ForeignKeyField("models.Region", related_name="cities", null=False)

    businesses: fields.BackwardFKRelation["Business"]
    phrases: fields.BackwardFKRelation["Phrase"]
    cities: fields.BackwardFKRelation["Region"]

    _icon = 'location'

    class Meta:
        table_description = "Countries/Cities"


class Topic(Model):
    id: int
    name: str = fields.CharField(127, unique=True)

    businesses: fields.BackwardFKRelation["Business"]
    phrases: fields.BackwardFKRelation["Phrase"]

    _icon = 'tag'

    class Meta:
        table_description = "Business types"


class Business(Model):
    id: int
    topic: fields.ForeignKeyRelation[Topic] = fields.ForeignKeyField("models.Topic", related_name="businesses")
    topic_id: int
    region: fields.ForeignKeyRelation[Region] = fields.ForeignKeyField("models.Region", related_name="businesses", null=True)
    region_id: int
    agent: fields.ForeignKeyRelation[Agent] = fields.ForeignKeyField("models.Agent", related_name="businesses", null=True)
    agent_id: int

    chats: fields.ManyToManyRelation["Chat"] = fields.ManyToManyField("models.Chat", 'chatinbusiness')
    clients: fields.BackwardFKRelation[Client]
    phrases: fields.BackwardFKRelation["Phrase"]

    _icon = 'briefcase'

    async def repr(self):
        return f'{(await self.topic).name}:{(await self.region).name}'

    class Meta:
        table_description = "Businesses - Topic in Regions"
        unique_together = (("topic_id", "region_id"),)


class ChatInBusiness(Model):
    business: fields.OneToOneRelation[Business] = fields.OneToOneField("models.Business")
    chat: fields.OneToOneRelation[Chat] = fields.OneToOneField("models.Chat")
    created_at: datetime = DatetimeSecField(auto_now_add=True)

    _icon = 'chat'
    _hidden = True

    class Meta:
        table_description = "Chats in business"


class Word(Model):
    txt: str = fields.CharField(255)
    # tag: str = fields.CharField(255) # todo pymorph

    _icon = 'alphabet-latin'

    _name = 'txt'

    class Meta:
        table_description = "Words (Phrase parts)"


class Phrase(Model):
    txt: str = fields.CharField(4095, unique=True)  # todo move to separate words
    business: fields.ForeignKeyRelation[Business] = fields.ForeignKeyField("models.Business", related_name="phrases", null=False)
    business_id: int
    topic: fields.ForeignKeyRelation[Topic] = fields.ForeignKeyField("models.Topic", related_name="phrases", null=False)
    topic_id: int
    region: fields.ForeignKeyRelation[Region] = fields.ForeignKeyField("models.Region", related_name="phrases", null=False)
    region_id: int
    is_excl: bool = fields.BooleanField(default=0)
    created_at: datetime = DatetimeSecField(auto_now_add=True)
    updated_at: datetime = DatetimeSecField(auto_now=True)

    _icon = 'alphabet-latin'

    def repr(self):
        return f'{self.is_excl and "! "}{self.txt}'

    class Meta:
        table_description = "Businesses - Topic in Regions"


class Text(Model):
    content: str = fields.CharField(4095, unique=True)
    # updated_at: datetime = DatetimeSecField(auto_now=True) # TODO write edits

    messages: fields.BackwardFKRelation["Msg"]
    heaps: fields.BackwardFKRelation["Heap"]

    _icon = 'message'

    def repr(self):
        return f'{self.content[:50]+".." if len(self.txt)>50 else self.txt}'

    class Meta:
        table_description = "Message"


class Heap(Model):
    id: int = fields.BigIntField(True)
    chat: str = fields.CharField(63, null=True)
    date: datetime = DatetimeSecField()
    link: str = fields.CharField(63, null=True)
    txt: fields.ForeignKeyRelation[Text] = fields.ForeignKeyField('models.Text', 'heaps')
    removed_at: datetime = DatetimeSecField(null=True)
    views: int = fields.SmallIntField()
    msg_in_chat: int = fields.IntField(null=True)
    # updated_at: datetime = DatetimeSecField(auto_now=True) # TODO write edits

    messages: fields.BackwardFKRelation["Msg"]

    _icon = 'message'

    def repr(self):
        return f'{self.chat or self.link}: {self.txt[:50]+".." if len(self.txt)>50 else self.txt}'

    class Meta:
        table_description = "Heap"


class Msg(Model):
    id: int = fields.BigIntField(pk=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", 'messages')
    chat: fields.ForeignKeyRelation[Chat] = fields.ForeignKeyField("models.Chat", 'messages')
    business: fields.ForeignKeyRelation[Business] = fields.ForeignKeyField('models.Business', 'messages')
    business_id: int
    removed_at: datetime = DatetimeSecField(null=True)
    heap: fields.ForeignKeyRelation[Heap] = fields.ForeignKeyField("models.Heap", 'messages')
    heap_id: int
    created_at: datetime = DatetimeSecField(auto_now_add=True)
    views: int = fields.IntField()
    link: str = fields.CharField(4095, unique=True)
    txt: fields.ForeignKeyRelation[Text] = fields.ForeignKeyField('models.Text', 'messages')
    # updated_at: datetime = DatetimeSecField(auto_now=True) # TODO write edits

    _icon = 'message'

    def repr(self):
        return f'{self.txt[:50]+".." if len(self.txt)>50 else self.txt}'

    class Meta:
        table_description = "Messages"


class Lead(Model):
    msg: fields.ForeignKeyRelation[Msg] = fields.ForeignKeyField("models.Msg", 'lead')
    msg_id: int
    phrase: fields.ForeignKeyRelation[Phrase] = fields.ForeignKeyField('models.Phrase', 'leads')
    phrase_id: int
    word: fields.ForeignKeyRelation[Word] = fields.ForeignKeyField('models.Word', 'leads')
    word_id: int

    _icon = 'done'

    _name = 'id'

    class Meta:
        table_description = "Leads"


@post_save(Phrase)
async def phrase_consist(
    sender: Type[Phrase], instance: Phrase, created: bool, using_db, update_fields
) -> None:
    if {'business_id', 'topic_id', 'region_id'} & update_fields:
        if instance.business_id:
            if instance.topic_id:
                print('No need to set topic if you set business!')
                instance.topic_id = None
            if instance.region_id:
                print('No need to set region if you set business!')
                instance.region_id = None
        if instance.topic_id and instance.region_id:
            print('No need to set topic and region. Then just set only business!')
            instance.business = await Business.get(topic=instance.topic, region=instance.region)
        await instance.save()
