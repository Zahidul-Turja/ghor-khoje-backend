from django.db import models
from user.models import User
from django.utils import timezone


class Conversation(models.Model):
    CONVERSATION_TYPES = [
        ("user_to_user", "User to User"),
        ("user_to_admin", "User to Admin"),
    ]

    conversation_type = models.CharField(
        max_length=20, choices=CONVERSATION_TYPES, default="user_to_user"
    )

    # For user-to-user conversations, both participants are stored
    # For user-to-admin conversations, user is the regular user, admin can be None (any admin can respond)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="conversations_as_user"
    )

    other_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="conversations_as_other_user",
        null=True,
        blank=True,
        help_text="For user-to-user conversations. Leave blank for user-to-admin conversations.",
    )

    # Optional: specific admin for user-to-admin conversations
    admin_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="admin_conversations",
        null=True,
        blank=True,
        limit_choices_to={"is_superuser": True},
        help_text="Specific admin for user-to-admin conversations (optional)",
    )

    title = models.CharField(
        max_length=200, blank=True, help_text="Optional conversation title"
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Status fields
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["conversation_type", "user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]

    def __str__(self):
        if self.conversation_type == "user_to_admin":
            admin_name = self.admin_user.full_name if self.admin_user else "Any Admin"
            return f"{self.user.full_name} → {admin_name}"
        else:
            other_name = self.other_user.full_name if self.other_user else "Unknown"
            return f"{self.user.full_name} ↔ {other_name}"

    def get_participants(self):
        """Return all participants in the conversation"""
        participants = [self.user]
        if self.other_user:
            participants.append(self.other_user)
        if self.admin_user:
            participants.append(self.admin_user)
        return participants

    def can_user_access(self, user):
        """Check if a user can access this conversation"""
        if user == self.user or user == self.other_user:
            return True
        if self.conversation_type == "user_to_admin" and user.is_superuser:
            return True
        return False


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )

    content = models.TextField(null=True, blank=True)

    # Message metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Message status
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # Optional: file attachment
    attachment = models.FileField(
        upload_to="chat_attachments/%Y/%m/%d/", null=True, blank=True
    )

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["conversation", "created_at"]),
            models.Index(fields=["sender", "created_at"]),
            models.Index(fields=["is_read"]),
        ]

    def __str__(self):
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"{self.sender.full_name}: {preview}"

    def mark_as_read(self):
        """Mark message as read"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=["is_read"])

    def can_user_edit(self, user):
        """Check if a user can edit this message"""
        return user == self.sender and not self.is_deleted

    def can_user_delete(self, user):
        """Check if a user can delete this message"""
        return user == self.sender or (
            self.conversation.conversation_type == "user_to_admin" and user.is_superuser
        )
