from forum.models import Question, Answer, QuestionVote, AnswerVote
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):

    votes = serializers.SerializerMethodField('count_votes')
    username = serializers.SerializerMethodField('get_username')
    user_obj = serializers.SerializerMethodField('get_user')
    timestamp = serializers.DateTimeField(read_only=True)
    hidden_to_user = serializers.SerializerMethodField('is_hidden')
    moderator = serializers.SerializerMethodField('is_moderator')

    class Meta:
        model = Question
        fields = ('id', 'title', 'course', 'answers', 'text', 'slug',
                  'votes', 'timestamp', 'username', 'user_obj', 'hidden',
                  'hidden_by', 'hidden_to_user', 'moderator', 'hidden_justification',)

    def count_votes(self, obj):
        if obj:
            return obj.count_votes
        else:
            return 0

    def get_username(self, obj):
        if obj:
            return obj.user.username
        else:
            return u''

    def get_user(self, obj):
        if obj:
            from accounts.serializers import TimtecUserSerializer
            tus = TimtecUserSerializer(obj.user)
            return tus.data
        else:
            return u''


    def is_hidden(self, obj):
        if hasattr(obj, 'hidden_to_user'):
            return obj.hidden_to_user
        return obj.hidden

    def is_moderator(self, obj):
        if hasattr(obj, 'moderator'):
            return obj.moderator
        return False


class AnswerSerializer(serializers.ModelSerializer):

    votes = serializers.SerializerMethodField('count_votes')
    username = serializers.SerializerMethodField('get_username')
    user_obj = serializers.SerializerMethodField('get_user')
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question', 'text', 'votes', 'timestamp', 'username', 'user_obj',)

    def count_votes(self, obj):
        if obj:
            return obj.count_votes
        else:
            return 0

    def get_username(self, obj):
        if obj:
            return obj.user.username
        else:
            return u''

    def get_user(self, obj):
        if obj:
            from accounts.serializers import TimtecUserSerializer
            tus = TimtecUserSerializer(obj.user)
            return tus.data
        else:
            return u''


class QuestionVoteSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = QuestionVote
        fields = ('question', 'timestamp', 'user', 'value')


class AnswerVoteSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AnswerVote
        fields = ('id', 'answer', 'timestamp', 'user', 'value')
