# import asyncio
import os
from json.decoder import JSONDecodeError
from pathlib import Path
import sys
import time
import traceback

from chat_downloader import ChatDownloader
from chat_downloader.errors import ChatDownloaderError
from chat_downloader.output.continuous_write import ContinuousWriter

from . import myutil as util
from .arguments import Arguments
from .videoinfo2 import VideoInfo
from .exceptions import InvalidVideoIdException, NoContents, PatternUnmatchError, ZeroDuration
from .progressbar import ProgressBar
from .youtube import channel
from .youtube import playlist


class Downloader:
    def __init__(self, dir_videos: set):
        self._dir_videos = dir_videos

    def video(self, video, splitter_string) -> None:
        is_complete = False
        video_id = video.get('id')
        try:
            if not os.path.exists(Arguments().output):
                raise FileNotFoundError
            separated_path = str(Path(Arguments().output)) + os.path.sep
            path = util.checkpath(separated_path + video_id + '.txt')
            # check if the video_id is already exists the output folder
            if video_id in self._dir_videos:
                # raise Exception(f"Video [{video_id}] is already exists in {os.path.dirname(path)}. Skip process.")
                print(
                    f"\nSkip the process...\n  The file for the video [{video_id}] already exists in {os.path.dirname(path)}.")
                sys.argv = []
                return

            skipmessage = None
            if video.get("duration") is None:
                skipmessage = "Unable to retrieve chat: Cannot retrieve the duration."

            elif video.get("duration") == 'LIVE':
                skipmessage = "Unable to retrieve chat: This stream is live."

            elif video.get("duration") == 'UPCOMING':
                skipmessage = "Unable to retrieve chat: This stream is upcoming."

            print(splitter_string)
            print(
                f"\n"
                f"[title]    {video.get('title')}\n"
                f"[id]       {video_id}    [published] {video.get('time_published')}\n"
                f"[channel]  {video.get('author')}"
            )
            print(f"[path]     {path}  [duration] {video.get('duration')}")
            if skipmessage:
                print(f"{skipmessage}\n")
                return
          

            duration = util.time_to_seconds(video["duration"])
            if duration == 0:
                raise ZeroDuration
            url = f"https://www.youtube.com/watch?v={video_id}"
            downloader = ChatDownloader(cookies=Arguments().cookie)
            chat = downloader.get_chat(url)
            writer = ContinuousWriter(
                path, indent=14, sort_keys=True, overwrite=True)

            pbar = ProgressBar(int(duration) * 1000, status='Extracting...'+" "*20)

            for item in chat:
                time_in_seconds = item.get('time_in_seconds')
                pbar._disp(None, time_in_seconds)
                writer.write(chat.format(item), flush=True)

            pbar.reset(total=1, status="Complete.   ")
            pbar._disp(None, 1)
            pbar.reset(status="Complete.")
            print()

            is_complete = True
            time.sleep(Arguments().interval_next)
        except ChatDownloaderError as err:
            
            self.checklog(splitter_string,video,"CE_"+type(err).__name__)
            print(type(err).__name__)
        except InvalidVideoIdException:
            self.checklog(splitter_string,video,"InvalidVideoIdException")
            print("Invalid Video ID or URL:", video_id)
        except NoContents as e:
            self.checklog(splitter_string,video,"NoContents")
            print(str(e)[:80])
        except FileNotFoundError:
            print("The specified directory does not exist.:{}".format(
                Arguments().output))
            exit(0)
        except (JSONDecodeError, PatternUnmatchError) as e:
            self.checklog(splitter_string,video,"JSONDecodeError",e.doc)
            print(type(e),str(e))
        except ZeroDuration:
            self.checklog(splitter_string,video,"ZeroDuration")
            print("Duration of this video is zero. Skip process.")
        except KeyboardInterrupt:
            is_complete = "KeyboardInterrupt"
        except Exception as e:
            self.checklog(splitter_string,video,"Exception")
            print(str(e))
        finally:
            # clear_tasks()
            return is_complete

    def videos(self, video_ids) -> None:
        for i, video_id in enumerate(video_ids):

            if '[' in video_id or ']' in video_id:
                video_id = video_id.replace('[', '').replace(']', '')
            try:
                video = self.get_info(video_id)
                time.sleep(Arguments().interval_info)
                if video.get('error'):
                    print("error")
                    continue
                splitter_string = f"\n{'-'*10} video:{i+1} of {min(len(video_ids),Arguments().first)} {'-'*10}"
                ret = self.video(video,splitter_string)
                if ret == "KeyboardInterrupt":
                    self.cancel()
                    return
            except InvalidVideoIdException:
                print(f"Invalid video id: {video_id}")
                continue
            # except KeyboardInterrupt:
            #     print("KeyboardInterrupt")
            #     exit(0)
            #     break

    def channels(self, channels, tab) -> None:
        for i, ch in enumerate(channels):
            counter = 0
            for video in channel.get_videos(channel.get_channel_id(ch), tab=tab):
                if counter > Arguments().first - 1:
                    break
                splitter_string = f"\n{'-'*10} channel: {i+1} of {len(channels)} / video: {counter+1} of {Arguments().first} {'-'*10}"
                ret = self.video(video, splitter_string)
                if ret == "KeyboardInterrupt":
                    self.cancel()
                    return
                if ret:
                    counter += 1
                    time.sleep(Arguments().interval_info)

    def playlist_ids(self, playlist_ids) -> None:
        stop=False
        for i, playlist_id in enumerate(playlist_ids):
            counter = 0
            page = 1
            video_list, num_pages, metadata = playlist.get_playlist_page(playlist_id,page=str(page))

            while True:
                for video in video_list:
                    if counter > Arguments().first - 1:
                        stop=True
                        break
                    splitter_string = f"\n{'-'*10} playlist: {i+1} of {len(playlist_ids)} / video: {counter+1} of {Arguments().first} {'-'*10}"
                    ret = self.video(video, splitter_string)
                    if ret == "KeyboardInterrupt":
                        self.cancel()
                        return
                    if ret:
                        counter += 1
                page += 1
                if stop or page > num_pages:
                    break
                video_list, num_pages, metadata = playlist.get_playlist_page(playlist_id,page=str(page))

                

    def cancel(self, ex=None, pbar=None):
        '''Called when keyboard interrupted has occurred.
        '''
        print("\nKeyboard interrupted.\n")
        if ex:
            ex.cancel()
        if pbar:
            pbar.cancel()
        exit(0)

    def get_info(self, video_id: str):
        video = dict()
        for i in range(3):
            try:
                info = VideoInfo(video_id)
                break
            except PatternUnmatchError:
                time.sleep(2)
                continue
        else:
            print(f"PatternUnmatchError:{video_id}")
            return {'error': True}

        video['id'] = video_id
        video['author'] = info.get_channel_name()
        video['time_published'] = "Unknown"
        video['title'] = info.get_title()
        video['duration'] = info.get_duration()
        return video

    def checklog(self,splitter_string,video,exception_type='',other_mes=''):
        if Arguments().save_error_data:
                util.save(splitter_string+
                        f"\n"
                        f"[title]    {video.get('title')}\n"
                        f"[id]       {video.get('id')}    [published] {video.get('time_published')}\n"
                        f"[channel]  {video.get('author')}\n\n"+
                        traceback.format_exc()+'\n'+
                        other_mes,
                        "Error", f"_{exception_type}.dat")
# def clear_tasks():
#     '''
#     Clear remained tasks.
#     Called when internal exception has occurred or
#     after each extraction process is completed.
#     '''
#     async def _shutdown():
#         tasks = [t for t in asyncio.all_tasks()
#                  if t is not asyncio.current_task()]
#         for task in tasks:
#             task.cancel()

#     try:
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(_shutdown())
#     except Exception as e:
#         print(e)
