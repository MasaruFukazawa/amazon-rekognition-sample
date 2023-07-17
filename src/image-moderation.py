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

    # 節度を超えた画像を検出する
    # .. バケット内にフォルダがある場合は、そのフォルダ内の画像も検出する
    for obj in bucket.objects.all():

        if obj.key.endswith('.jpg') or obj.key.endswith('.png'):
            print('Image: {}'.format(obj.key))

            # aws rekognitionを利用して画像を分析する
            response = rekognition.detect_moderation_labels(
                Image={
                    'S3Object': {
                        'Bucket': bucket.name,
                        'Name': obj.key
                    }
                },
                MinConfidence=50
            )

            # 結果を表示する
            print('Labels:')

            for label in response['ModerationLabels']:
                print('  - {}'.format(label['Name']))
                print('    Confidence: {}'.format(label['Confidence']))
                print('    Parent: {}'.format(label['ParentName']))

            print('----------')


if __name__ == '__main__':
    main()