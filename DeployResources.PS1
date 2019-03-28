Login-AzureRmAccount
New-AzureRmResourceGroup -Name Contoso_IaaS_Chenjian -Location westeurope
$parameters = @{}
Add-Type -Assembly 'System.Windows.Forms'
Add-Type -Assembly 'System.Drawing'


$form = New-Object Windows.Forms.Form

$txt = "Enter a password for the lab VM's. 
Passwords must be 12 - 123 characters in length and meet 3 out of the following 4 complexity requirements: 

* Have lower characters 
* Have upper characters 
* Have a digit 
* Have a special character"

$label1 = new-object System.Windows.Forms.Label
$label1.AutoSize = $true
$label1.Location = new-object System.Drawing.Point(12, 19)
$label1.Name = "label1"
$label1.Size = new-object System.Drawing.Size(514, 78)
$label1.TabIndex = 0
$label1.Text = $txt


$label2 = new-object System.Windows.Forms.Label
$label2.AutoSize = $true
$label2.ForeColor = [System.Drawing.Color]::Red
$label2.Location = new-object System.Drawing.Point(48, 180)
$label2.Name = "label2"
$label2.Size = new-object System.Drawing.Size(335, 13)
$label2.TabIndex = 1
$label2.Text = "Please remember this password as it will be used to login to IaaS VM's"

$maskedTextBox1 = new-object System.Windows.Forms.MaskedTextBox
$maskedTextBox1.Location = new-object System.Drawing.Point(124, 118)
$maskedTextBox1.Name = "maskedTextBox1"
$maskedTextBox1.PasswordChar = '*'
$maskedTextBox1.Size = new-object System.Drawing.Size(174, 20)
$maskedTextBox1.TabIndex = 2

$maskedTextBox2 = new-object System.Windows.Forms.MaskedTextBox
$maskedTextBox2.Location = new-object System.Drawing.Point(124, 144)
$maskedTextBox2.Name = "maskedTextBox2"
$maskedTextBox2.PasswordChar = '*'
$maskedTextBox2.Size = new-object System.Drawing.Size(174, 20)
$maskedTextBox2.TabIndex = 3

$label3 = new-object System.Windows.Forms.Label
$label3.AutoSize = $true
$label3.Location = new-object System.Drawing.Point(65, 121)
$label3.Name = "label3"
$label3.Size = new-object System.Drawing.Size(53, 13)
$label3.TabIndex = 4
$label3.Text = "Password"

$label4 = new-object System.Windows.Forms.Label
$label4.AutoSize = $true
$label4.Location = new-object System.Drawing.Point(27, 147)
$label4.Name = "label4"
$label4.Size = new-object System.Drawing.Size(91, 13)
$label4.TabIndex = 5
$label4.Text = "Confirm Password"


$button1 = new-object System.Windows.Forms.Button
$button1.Location = new-object System.Drawing.Point(444, 169)
$button1.Name = "button1"
$button1.Size = new-object System.Drawing.Size(82, 39)
$button1.TabIndex = 6
$button1.Text = "Submit"
$button1.UseVisualStyleBackColor = $true
$button1.Add_Click({
           

           if(!($maskedTextBox1.Text -eq $maskedTextBox2.Text))
           {
                [System.Windows.Forms.MessageBox]::Show("Passwords do not match" , "Error")
           }
           
           else
           {
               $score = 0
               if($maskedTextBox1.Text -match '[0-9]'){$score++}
               if($maskedTextBox1.Text -cmatch '[a-z]'){$score++}
               if($maskedTextBox1.Text -cmatch '[A-Z]'){$score++}
               if($maskedTextBox1.Text -match '[\W_]'){$score++}
               if($maskedTextBox1.Text.Length -lt 12 -or $maskedTextBox1.Text.Length -gt 123){$score = 0}
               
               if($score -ge 3)
               {
                    $pwd = ConvertTo-SecureString -String $maskedTextBox1.Text -AsPlainText -Force
                    
                    $parameters.Add(“adminPassword”, $pwd)
                    $form.Close()
                    
               }
               else
               {
                     [System.Windows.Forms.MessageBox]::Show("Password does not meet length/complexity requirements" , "Error")
               }
           }
    })

$form.ClientSize = new-object System.Drawing.Size(570, 230)
$form.Controls.Add($button1)
$form.Controls.Add($label4)
$form.Controls.Add($label3)
$form.Controls.Add($maskedTextBox2)
$form.Controls.Add($maskedTextBox1)
$form.Controls.Add($label2)
$form.Controls.Add($label1)
$form.Text = "Enter password"
$form.ShowDialog()

Write-Host "Deploying ARM template, this may take up to 45 minutes to complete...." -ForegroundColor Green
New-AzureRmResourceGroupDeployment -verbose -Name LAB_Chenjian -ResourceGroupName Contoso_IaaS_Chenjian -TemplateFile C:\Workshop\Module1\lab.json -TemplateParameterObject $parameters
