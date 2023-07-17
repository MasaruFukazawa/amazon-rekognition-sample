#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import boto3


def main():
    """ エントリーポイント
    """

    s3 = boto3.resource('s3', region_name=os.environ['AWS_REGION'])
    bucket = s3.Bucket('amazon-rekognition-sample')

    rekognition = boto3.client('rekognition', region_name=os.environ['AWS_REGION'])

    # 画像からテキストを検出する
    # .. バケット内にフォルダがある場合は、そのフォルダ内の画像も検出する
    for obj in bucket.objects.all():
            
            if obj.key.startswith('text-detection/') and (obj.key.endswith('.jpg') or obj.key.endswith('.png')):

                print('Image: {}'.format(obj.key))
    
                # aws rekognitionを利用して画像を分析する
                response = rekognition.detect_text(
                    Image={
                        'S3Object': {
                            'Bucket': bucket.name,
                            'Name': obj.key
                        }
                    }
                )
    
                # 結果を表示する
                print('Text:')
                print(response['TextDetections'])
                print('----------')

if __name__ == '__main__':
    main()