from sqlalchemy.orm import Session

from app.models.user_interaction import (
    InteractionType,
    UserInteraction,
)


class InteractionService:

    INTERACTION_WEIGHTS = {
        InteractionType.SEARCH: 1,
        InteractionType.VIEW: 2,
        InteractionType.CHAT_REFERENCE: 5,
        InteractionType.UPDATE: 3,
        InteractionType.DELETE: 1,
        InteractionType.FAVORITE: 10,
        InteractionType.ARCHIVE: 1,
    }

    def record_interaction(
        self,
        db: Session,
        user_id: int,
        memory_id: int,
        interaction_type: InteractionType,
    ):
        interaction = UserInteraction(
            user_id=user_id,
            memory_id=memory_id,
            interaction_type=interaction_type.value,
            weight=self.INTERACTION_WEIGHTS[
                interaction_type
            ],
        )

        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        return interaction

    def get_memory_interactions(
        self,
        db: Session,
        memory_id: int,
    ):
        return (
            db.query(UserInteraction)
            .filter(
                UserInteraction.memory_id
                == memory_id
            )
            .all()
        )

    def get_user_interactions(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(UserInteraction)
            .filter(
                UserInteraction.user_id
                == user_id
            )
            .all()
        )

    def calculate_total_weight(
        self,
        db: Session,
        memory_id: int,
    ):
        interactions = (
            self.get_memory_interactions(
                db,
                memory_id,
            )
        )

        return sum(
            interaction.weight
            for interaction in interactions
        )


interaction_service = InteractionService()