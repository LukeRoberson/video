"""
Check if a video exists in the database.
"""

import sys
import os
from colorama import Style, Fore

# Add the parent folder to the Python path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

from sql_db import (  # noqa: E402
    DatabaseContext,
    VideoManager,
)

video_list = [
    # Oct 2014
    "JW Broadcasting—October 2014",
    "Behind the Scenes of JW Broadcasting",
    "M. Stephen Lett: Young Ones​—You Are Loved by Jehovah",
    "Act Wisely When Bullied",
    "Theodore Jaracz: Enduring Persecution Brings Blessings",
    "Tour of the Legal Department at World Headquarters",
    "William Malenfant: Run the Race With Endurance (1 Cor. 9:24)",
    "Burt Mann: I Have Finally Become Something",
    "The Best Life Ever",

    # Nov 2014
    "Lloyd Barry: Life as a Missionary in Japan",
    "The Gournons: Seek First the Kingdom",
    "Kenneth Flodin: Curb Wrong Desires Immediately (Matt. 19:6)",
    "We Won’t Forget You",

    # Dec 2014
    "David H. Splane: Prepare to Sing the New Songs",
    "\"There Is More Happiness in Giving\"",
    "Max Larson: Never Thought of Anything Else",
    "Tour of the Central Europe Branch",
    "M. Stephen Lett: Beware of Overconfidence (1 Cor. 10:12)",
    "James Dyson: Jehovah Is Kind and Merciful",

    # Feb 2015
    "Samuel F. Herd: United​—In Spirit and in Thinking",
    "An Assembly in Their Mother Tongue",
    "Showing Hospitality at International Conventions",
    "Behind the Scenes With Convention Volunteers",
    "Differences Between Special and International Conventions",
    "David H. Splane: Unity Breaks Down Barriers (Rom. 3:29)",
    "Love and Respect Unite Families",
    "Forest James: A Medicine Man Encouraged Me to Read the Bible",
    "Lyman Swingle: Producing The New World Society in Action",
    "Older Ones—You Have an Important Role",
    "If You Could See What I See",

    # Mar 2015
    "Gerrit Lösch: Fortified by \"the Prophetic Word\"",
    "Speeding Up the Distribution of Literature",
    "George Couch: This Is Jehovah's Organization",
    "Serving Jehovah in a Divided Household Is Possible",
    "A Bible Exhibit That Glorifies Jehovah’s Name",
    "Nancy Simon: God's Kingdom Is the Only Solution",
    "Central Europe Branch Report",
    "What Means the Most to Me",

    # Apr 2015
    "South Africa Branch Expansion Report",
    "Mark Sanderson: We Continually Remember Your Endurance",
    "The Kalins: Printing Under Ban in Siberia",
    "The Namgungs: Imprisoned for Their Faith",
    "John Foster: Doing the Very Best I Can",
    "Priscilla Lagno: He Told Me Not to Come Home",
    "Encourage Your Mate \"Without a Word\"",
    "The Hopkinsons: Enduring for Decades as Missionaries",
    "David Schafer: Enduring the Imperfections of Others (Phil. 4:6)",
    "Never Give Up",

    # May 2015
    "M. Stephen Lett: \"Honor Jehovah With Your Valuable Things\"",
    "‘A Gift in Hand to Jehovah’",
    "Jehovah Will Care for Our Needs",
    "Helping Our Brothers When Disaster Strikes",
    "Helping the Blind Learn the Truth",
    "John Lewis: Something Was Missing in My Life",
    "Tour of the Japan Branch Writing Desk",
    "Remote Translation Offices Help Spread the Kingdom News",
    "Reaching Many at a Book Fair",
    "Experiences From Mauritius, Madagascar, and Zimbabwe",
    "“Honor Jehovah With Your Valuable Things”"
]

with DatabaseContext() as db:
    video_mgr = VideoManager(db)

    for video_name in video_list:
        # Check if the video exists
        video_id = video_mgr.name_to_id(video_name)

        if video_id is None:
            print(
                Fore.RED,
                f"Video '{video_name}' not found.",
                Style.RESET_ALL
            )
        else:
            print(
                Fore.GREEN,
                f"Video '{video_name}' exists with ID: {video_id}",
                Style.RESET_ALL
            )
