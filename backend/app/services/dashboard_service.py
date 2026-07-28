from sqlalchemy.orm import Session

from app.services.analytics_service import analytics_service


class DashboardService:
    def get_dashboard_summary(
        self,
        db: Session,
        user_id: int,
    ):
        statistics = analytics_service.get_memory_statistics(
            db=db,
            user_id=user_id,
        )

        categories = analytics_service.get_category_distribution(
            db=db,
            user_id=user_id,
        )

        # Ignore memories that don't have a category assigned
        valid_categories = [
            category
            for category in categories
            if category["category"] is not None
        ]

        top_category = None
        least_category = None

        if valid_categories:
            sorted_categories = sorted(
                valid_categories,
                key=lambda x: x["count"],
                reverse=True,
            )

            top_category = sorted_categories[0]["category"]
            least_category = sorted_categories[-1]["category"]

        total = statistics["total_memories"]
        archived = statistics["archived_memories"]

        archive_percentage = 0

        if total > 0:
            archive_percentage = round(
                (archived / total) * 100,
                2,
            )

        if top_category:
            insight = (
                f"Most memories belong to '{top_category}'. "
                f"{archive_percentage}% of memories are archived."
            )
        else:
            insight = (
                f"No categorized memories found. "
                f"{archive_percentage}% of memories are archived."
            )

        return {
            **statistics,
            "top_category": top_category,
            "least_used_category": least_category,
            "archive_percentage": archive_percentage,
            "insight": insight,
        }


dashboard_service = DashboardService()