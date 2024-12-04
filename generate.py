# import modules
import qrcode
from PIL import Image, ImageDraw, ImageFont
import click

@click.command()
@click.option('--logo-path', default='logos/github/github-mark.png', help='Path to the logo image.')
@click.option('--url', default='https://github.com/saniamos/', help='URL or text to encode in the QR code.')
@click.option('--qr-color', default='#24292f', help='Color of the QR code.')
@click.option('--output', default='codes/github.png', help='Output file name for the generated QR code.')
@click.option('--include-url', is_flag=True, help='Include the URL text at the bottom of the QR code.')
def generate_qr(logo_path, url, qr_color, output, include_url):
    # taking image which user wants in the QR code center
    logo = Image.open(logo_path)

    # convert transparency to white
    if logo.mode in ('RGBA', 'LA') or (logo.mode == 'P' and 'transparency' in logo.info):
        alpha = logo.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", logo.size, (255, 255, 255) + (255,))
        bg.paste(logo, mask=alpha)
        logo = bg.convert('RGB')

    # create a white border and make the image square
    max_dim = max(logo.size)
    border_size = int(0.15 * max_dim)
    logo_with_border = Image.new('RGB', (max_dim + 2 * border_size, max_dim + 2 * border_size), 'white')
    logo_with_border.paste(logo, ((max_dim - logo.size[0]) // 2 + border_size, (max_dim - logo.size[1]) // 2 + border_size))

    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )

    # adding URL or text to QRcode
    QRcode.add_data(url)

    # generating QR code
    QRcode.make()

    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=qr_color, back_color="white").convert('RGB')

    # calc the amount of squares the image should take up
    # overall the image should take up 25% and as it is centered, so that left and right of center are the same amounts covered
    assert QRcode.modules_count % 2 == 1, "I'm assuming there is always a center row"
    logo_size = (int(QRcode.modules_count * .125) * 2 + 1) * QRcode.box_size

    # resize logo_with_border to fit the QR code grid
    logo_with_border = logo_with_border.resize((logo_size, logo_size), Image.LANCZOS)

    # set size of QR code
    pos = ((QRimg.size[0] - logo_with_border.size[0]) // 2,
           (QRimg.size[1] - logo_with_border.size[1]) // 2)
    QRimg.paste(logo_with_border, pos)

    if include_url:
        # extend the canvas to add the URL at the bottom
        new_height = QRimg.size[1] + 40  # Add space for the text
        extended_img = Image.new('RGB', (QRimg.size[0], new_height), 'white')
        extended_img.paste(QRimg, (0, 0))

        # draw the URL text at the bottom
        draw = ImageDraw.Draw(extended_img)
        draw.text((QRimg.size[1] // 2, QRimg.size[1] - 10), url, fill=qr_color, font_size=15, anchor="mt")
        QRimg = extended_img

    # save the QR code generated
    QRimg.save(output)

    print(f'Generated: {url}')

if __name__ == '__main__':
    generate_qr()