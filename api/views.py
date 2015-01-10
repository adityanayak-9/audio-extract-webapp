# coding=utf-8
import os
import subprocess
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.classes import CalcClass
import tempfile
from django.http import HttpResponse

UPLOAD_FOLDER = "/tmp/rest_ws/"
ALLOWED_EXTENSIONS = ('mp4', )


def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


class MyRESTView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        get_arg1 = request.GET.get('arg1', None)
        get_arg2 = request.GET.get('arg2', None)

        # Any URL parameters get passed in **kw
        myClass = CalcClass(get_arg1, get_arg2, *args, **kw)
        result = myClass.do_work()
        response = Response(result, status=status.HTTP_200_OK)
        return response


class MyConverterFromLocalView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']
        print file_obj.name
        # call(["ls", "-l"])
        print "begin process"

        if file_obj and allowed_file(file_obj.name):
            print "begin if"
            filename = file_obj.name
            # f = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
            # print f.name
            # f.close()
            filename = UPLOAD_FOLDER + file_obj.name
            ensure_dir(filename)
            with open(filename, 'wb+') as temp_file:
                for chunk in file_obj.chunks():
                    temp_file.write(chunk)
            print("file saved to disk under", filename)
            # file_obj.save(os.path.join(MEDIA_ROOT, filename)) # save the original mp4 file into the upload folder
            # print "saved"
            filename_without_extension = os.path.splitext(file_obj.name)[0]
            print "file without extension created"
            valid_filename = "".join(x for x in filename_without_extension if x.isalnum())
            # if valid_filename == "":
            #     valid_filename = tempfile.NamedTemporaryFile()
            new_filename = UPLOAD_FOLDER + valid_filename + '.mp3' # name of the destination file (.mp3)
            print "new filename"
            # call to the external command ffmpeg
            sp = subprocess.Popen(['ffmpeg', '-i', filename, new_filename], stdout=subprocess.PIPE)
            sp.wait()  # wait till the video converting ends
            # once the mp3 file is created, it will be opened and wrapped in the http response
            print "everything completed successfully"
            res = open(new_filename, 'rb')
            raw_res = res.read()
            response = HttpResponse(raw_res)
            res.close()
            response['Content-Length'] = str(os.stat(new_filename).st_size)
            response['Content-Type'] = "application/octet-stream"
            response['Content-Disposition'] = "inline; filename=" + new_filename
            return response
        else:
            print "file extension error"
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        # return Response(status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('''
            <!DOCTYPE html>
            <head>
                <title>Extraction audio à partir d'une video locale</title>
            </head>
            <body>
                <h1>Extraire Audio à partir d'une video locale</h1>
                <form action="" method="post" enctype="multipart/form-data">
                <p><input type="file" name="file">
                <input type="submit" value="Envoyer pour extraction"></p>
                </form>
            </body>
            ''')


class MyConverterFromYoutubeView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            youtube_link = request.data['youtube_link']
            print youtube_link
            print "begin process"
            # call to the external command youtube-dl
            command = "youtube-dl -x --audio-format mp3 " + youtube_link
            command0 = "youtube-dl --get-filename " + youtube_link
            sp = subprocess.Popen(command, shell=True)
            sp.wait()  # wait till the video converting ends
            sp2 = subprocess.Popen(command0, shell=True, stdout=subprocess.PIPE)
            sp2.wait()
            filename = sp2.communicate()[0].split('\n', 1)[0]
            output_filename = os.path.splitext(filename)[0] + ".mp3"
            print output_filename
            print "done"
            # once the mp3 file is created, it will be opened and wrapped in the http response
            print "everything completed successfully"
            res = open(output_filename, 'rb')
            raw_res = res.read()
            response = HttpResponse(raw_res)
            res.close()
            response['Content-Length'] = str(os.stat(output_filename).st_size)
            response['Content-Type'] = "application/octet-stream"
            response['Content-Disposition'] = "inline; filename=" + output_filename
            return response
        except Exception:
            print "error occurred"
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        # return Response(status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('''
            <!DOCTYPE html>
            <head>
                <title>Extraction audio à partir d'une video youtube</title>
            </head>
            <body>
                <h1>Extraire Audio à partir d'une video youtube</h1>
                <form action="" method="post" enctype="multipart/form-data">
                <p>Lien youtube:
                <input type="text" name="youtube_link">
                <input type="submit" value="Envoyer pour extraction"></p>
                </form>
            </body>
            ''')