import streamlit as st

def gen_filter(segments, target_width, target_height,transition_type, transition_value, transition_duration ,with_audio=False):
    video_fades = ""
    audio_fades = ""
    settb = ""
    last_fade_output = "0v"
    last_audio_output = "0:a"

    video_length = 0
    file_lengths = [0] * len(segments)

    if target_width:
        for i in range(len(segments)):
            # 视频归一化
            # settb += "[%d:v]settb=AVTB,fps=30,scale=w=%d:h=%d:force_original_aspect_ratio=1,pad=%d:%d:(ow-iw)/2:(oh-ih)/2[%dv];" % (i, target_width, target_height, target_width, target_height, i)
            settb += "[%d:v]settb=AVTB,scale=w=%d:h=%d:force_original_aspect_ratio=1,pad=%d:%d:(ow-iw)/2:(oh-ih)/2[%dv];" % (
            i, target_width, target_height, target_width, target_height, i)

    str_list = [str(f) for f in segments]
    print("转场视频长度：" + " ".join(str_list))
    for i in range(len(segments) - 1):
        file_lengths[i] = segments[i]

        video_length += float(file_lengths[i])
        next_fade_output = "v%d%d" % (i, i + 1)
        video_fades += f"[%s][%dv]{transition_type}=transition=%s:duration=%f:offset=%f%s%s" % \
                       (last_fade_output, i + 1, transition_value, float(transition_duration), video_length - float(transition_duration) * (i + 1),
                        '[' + next_fade_output + '];' if (i) < len(segments) - 2 else "",
                        "" if i < len(segments) - 2 else ",format=yuv420p[video];")
        last_fade_output = next_fade_output

        if with_audio:
            next_audio_output = "a%d%d" % (i, i + 1)
            # audio_fades += "[%s][%d:a]acrossfade=d=%f%s" % \
            # 第二段音频不需要淡入效果
            audio_fades += "[%s][%d:a]acrossfade=d=%f:c2=nofade%s" % \
                           (last_audio_output, i + 1, transition_duration,
                            '[' + next_audio_output + '];' if (i) < len(segments) - 2 else "[audio]")
            # 直接concat 不做效果处理
            # audio_fades += "[%s][%d:a]concat=n=2:v=0:a=1%s" % \
            #                (last_audio_output, i + 1,
            #                 '[' + next_audio_output + '];' if (i) < len(segments) - 2 else "[audio]")
            last_audio_output = next_audio_output

    if with_audio:
        return settb + video_fades + audio_fades
    return settb + video_fades
