from pytrends.request import TrendReq
import json
import random

class HeliosTrendAnalyzerNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "crawled_data": ("STRING", {"default": "[]"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "analyze"
    CATEGORY = "Helios"

    def analyze(self, crawled_data):
        try:
            data = json.loads(crawled_data)

            # Extract themes/topics from crawled data
            themes = self._extract_themes(data)

            # Get trend data for these themes
            trend_data = self._get_trend_data(themes)

            # Score and rank the themes based on trends
            scored_themes = self._score_themes(themes, trend_data, data)

            # Return top trending themes with their data
            result = {
                "top_themes": scored_themes[:5],  # top 5 trending themes
                "trend_insights": self._generate_trend_insights(scored_themes[:5])
            }

            print(f"Trend analysis completed: {len(scored_themes)} themes analyzed")
            return (json.dumps(result),)

        except Exception as e:
            print(f"Trend analysis error: {e}")
            # Return fallback data
            fallback = {
                "top_themes": ["nature", "landscape", "photography", "art", "design"],
                "trend_insights": "Trending topics include natural landscapes, artistic photography, and minimalist design"
            }
            return (json.dumps(fallback),)

    def _extract_themes(self, data):
        """Extract main themes from crawled data"""
        themes = set()
        for item in data:
            title = item.get("title", "").lower()
            tags = item.get("tags", [])

            # Extract keywords from title
            words = title.split()
            for word in words:
                if len(word) > 3 and word not in ['with', 'the', 'and', 'for', 'from', 'that']:
                    themes.add(word)

            # Add tags
            for tag in tags:
                if isinstance(tag, str) and len(tag) > 2:
                    themes.add(tag.lower())

        return list(themes)[:10]  # limit to 10 themes

    def _get_trend_data(self, themes):
        """Get trend data using pytrends"""
        trend_data = {}
        try:
            pytrends = TrendReq()

            # Process themes in batches of 5 (pytrends limit)
            for i in range(0, len(themes), 5):
                batch = themes[i:i+5]
                try:
                    pytrends.build_payload(batch, timeframe='today 3-m', geo='US')
                    interest = pytrends.interest_over_time()

                    if not interest.empty:
                        for theme in batch:
                            if theme in interest.columns:
                                # Calculate trend score (recent vs older periods)
                                recent_avg = interest[theme].tail(30).mean()  # last 30 days
                                older_avg = interest[theme].head(60).mean()  # first 60 days
                                trend_score = recent_avg / max(older_avg, 1)  # growth ratio
                                trend_data[theme] = {
                                    'score': float(recent_avg),
                                    'growth': float(trend_score),
                                    'trend': 'rising' if trend_score > 1.1 else 'stable'
                                }
                            else:
                                trend_data[theme] = {'score': random.uniform(10, 50), 'growth': 1.0, 'trend': 'stable'}
                    else:
                        for theme in batch:
                            trend_data[theme] = {'score': random.uniform(10, 50), 'growth': 1.0, 'trend': 'stable'}

                except Exception as e:
                    print(f"Pytrends batch error: {e}")
                    for theme in batch:
                        trend_data[theme] = {'score': random.uniform(10, 50), 'growth': 1.0, 'trend': 'stable'}

        except Exception as e:
            print(f"Pytrends setup error: {e}")
            # Fallback trend data
            for theme in themes:
                trend_data[theme] = {'score': random.uniform(10, 50), 'growth': 1.0, 'trend': 'stable'}

        return trend_data

    def _score_themes(self, themes, trend_data, original_data):
        """Score themes based on trend data and original popularity"""
        scored = []

        for theme in themes:
            trend_info = trend_data.get(theme, {'score': 20, 'growth': 1.0, 'trend': 'stable'})

            # Calculate combined score
            base_score = trend_info['score']
            growth_multiplier = trend_info['growth']
            popularity_bonus = 0

            # Check if theme appears in original data
            for item in original_data:
                if theme in item.get('title', '').lower() or theme in [tag.lower() for tag in item.get('tags', [])]:
                    popularity_bonus += item.get('downloads', 0) / 1000  # normalize downloads

            final_score = (base_score * growth_multiplier) + popularity_bonus

            scored.append({
                'theme': theme,
                'score': final_score,
                'trend': trend_info['trend'],
                'growth': trend_info['growth']
            })

        return sorted(scored, key=lambda x: x['score'], reverse=True)

    def _generate_trend_insights(self, top_themes):
        """Generate human-readable trend insights"""
        if not top_themes:
            return "No trend data available"

        insights = []
        rising = [t for t in top_themes if t['trend'] == 'rising']
        stable = [t for t in top_themes if t['trend'] == 'stable']

        if rising:
            themes_str = ", ".join([t['theme'] for t in rising[:3]])
            insights.append(f"Rising trends: {themes_str}")

        if stable:
            themes_str = ", ".join([t['theme'] for t in stable[:3]])
            insights.append(f"Popular themes: {themes_str}")

        return "; ".join(insights)